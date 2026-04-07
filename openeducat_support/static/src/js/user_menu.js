/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";
// Ensure standard items are registered before we replace them
import "@web/webclient/user_menu/user_menu_items"; // eslint-disable-line no-unused-vars

const userMenuRegistry = registry.category("user_menuitems");

function openeducatDocumentationItem() {
    const url = "http://doc.openeducat.org/";
    return {
        type: "item",
        id: "documentation",
        description: _t("Documentation"),
        href: url,
        callback: () => browser.open(url, "_blank"),
        sequence: 10,
    };
}

function openeducatSupportItem() {
    const url = "https://www.openeducat.org/page/support";
    return {
        type: "item",
        id: "support",
        description: _t("Support"),
        href: url,
        callback: () => browser.open(url, "_blank"),
        sequence: 20,
    };
}

function openeducatAccountItem() {
    const url = "https://www.openeducat.org/web/login";
    return {
        type: "item",
        id: "account",
        description: _t("My OpenEduCat account"),
        href: url,
        callback: () => browser.open(url, "_blank"),
        sequence: 60,
    };
}

userMenuRegistry.add("documentation", openeducatDocumentationItem, { force: true });
userMenuRegistry.add("support", openeducatSupportItem, { force: true });
userMenuRegistry.add("odoo_account", openeducatAccountItem, { force: true });
