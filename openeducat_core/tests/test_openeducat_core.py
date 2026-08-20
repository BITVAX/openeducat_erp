from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
from datetime import date, timedelta


@tagged('post_install', '-at_install')
class TestOpeneducatCore(TransactionCase):
    """Tests for openeducat_core models: course, batch, category, subject,
    student, faculty, subject_registration."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.categ = cls.env['product.category.public'].create({'name': 'Edu Test'})
        cls.category = cls.env['op.category'].create({
            'name': 'Test Category', 'code': 'TCAT',
        })
        cls.course = cls.env['op.course'].create({
            'name': 'Computer Science',
            'code': 'CS',
            'fullname': 'Bachelor of Computer Science',
            'category_id': cls.categ.id,
            'description': '<p>CS course</p>',
            'short_description': '<p>CS</p>',
        })
        cls.batch = cls.env['op.batch'].create({
            'name': 'Batch 2026',
            'code': 'B26',
            'course_id': cls.course.id,
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=180),
        })
        cls.subject = cls.env['op.subject'].create({
            'name': 'Programming 101',
            'code': 'PRG101',
            'course_id': cls.course.id,
        })
        cls.student = cls.env['op.student'].create({
            'name': 'Test Student',
            'firstname': 'Test',
            'lastname': 'Student',
            'course_detail_ids': [(0, 0, {
                'course_id': cls.course.id,
                'batch_id': cls.batch.id,
                'roll_number': 'R001',
            })],
        })
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Test Faculty Employee',
        })
        cls.faculty = cls.env['op.faculty'].create({
            'name': 'Test Faculty',
            'firstname': 'Test',
            'lastname': 'Faculty',
            'emp_id': cls.employee.id,
        })

    # ── Category ──────────────────────────────────────────

    def test_category_create(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.code, 'TCAT')

    # ── Course ────────────────────────────────────────────

    def test_course_create(self):
        self.assertEqual(self.course.code, 'CS')
        self.assertTrue(self.course.active)

    def test_course_display_name(self):
        self.assertIn('Computer Science', self.course.display_name)

    def test_course_topic(self):
        topic = self.env['op.course.topic'].create({
            'name': 'Intro to Python',
            'course_id': self.course.id,
            'sequence': 1,
        })
        self.assertEqual(topic.course_id, self.course)

    # ── Batch ─────────────────────────────────────────────

    def test_batch_create(self):
        self.assertEqual(self.batch.code, 'B26')
        self.assertEqual(self.batch.course_id, self.course)
        self.assertTrue(self.batch.active)

    def test_batch_display_name(self):
        # batch has custom _compute_display_name: [CODE-CODE] Course (Batch)
        self.assertIn('Batch 2026', self.batch.display_name)

    def test_batch_end_date_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['op.batch'].create({
                'name': 'Bad Batch',
                'code': 'BB',
                'course_id': self.course.id,
                'start_date': date.today(),
                'end_date': date.today() - timedelta(days=1),
            })

    # ── Subject ───────────────────────────────────────────

    def test_subject_create(self):
        self.assertEqual(self.subject.code, 'PRG101')
        self.assertEqual(self.subject.course_id, self.course)

    # ── Student ───────────────────────────────────────────

    def test_student_create_sets_partner(self):
        self.assertTrue(self.student.partner_id)
        self.assertTrue(self.student.partner_id.student)

    def test_student_course_detail(self):
        self.assertEqual(len(self.student.course_detail_ids), 1)
        detail = self.student.course_detail_ids[0]
        self.assertEqual(detail.course_id, self.course)
        self.assertEqual(detail.batch_id, self.batch)
        self.assertEqual(detail.roll_number, 'R001')

    def test_student_birthdate_future_raises(self):
        with self.assertRaises(ValidationError):
            self.student.birth_date = date.today() + timedelta(days=1)

    def test_student_birthdate_past_ok(self):
        self.student.birth_date = date(2000, 1, 15)
        self.assertEqual(self.student.birth_date, date(2000, 1, 15))

    # ── Faculty ───────────────────────────────────────────

    def test_faculty_create(self):
        self.assertEqual(self.faculty.emp_id, self.employee)
        self.assertTrue(self.faculty.active)

    # ── Subject Registration workflow ─────────────────────

    def test_registration_workflow(self):
        reg = self.env['op.subject.registration'].create({
            'student_id': self.student.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
            'compulsory_subject_ids': [(6, 0, [self.subject.id])],
        })
        self.assertEqual(reg.state, 'draft')
        self.assertNotEqual(reg.name, 'New')

        reg.action_submitted()
        self.assertEqual(reg.state, 'submitted')

        reg.action_approve()
        self.assertEqual(reg.state, 'approved')
        # Verify subject was linked to student course
        sc = self.env['op.student.course'].search([
            ('student_id', '=', self.student.id),
            ('course_id', '=', self.course.id),
        ], limit=1)
        self.assertIn(self.subject.id, sc.subject_ids.ids)

    def test_registration_reject_and_reset(self):
        reg = self.env['op.subject.registration'].create({
            'student_id': self.student.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
        })
        reg.action_submitted()
        reg.action_reject()
        self.assertEqual(reg.state, 'rejected')

        reg.action_reset_draft()
        self.assertEqual(reg.state, 'draft')

    def test_registration_approve_no_course_raises(self):
        student2 = self.env['op.student'].create({'name': 'No Course Student'})
        reg = self.env['op.subject.registration'].create({
            'student_id': student2.id,
            'course_id': self.course.id,
            'batch_id': self.batch.id,
        })
        reg.action_submitted()
        with self.assertRaises(ValidationError):
            reg.action_approve()
