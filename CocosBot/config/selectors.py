# Selectores de Login
LOGIN_SELECTORS = {
    "email_input": 'input[type="email"]',
    "password_input": 'input[type="password"]',
    "submit_button": 'button[type="submit"]',
    "two_factor_container": 'input#input0',
    "save_device_button": 'button:has-text("Sí, guardar como dispositivo seguro")',
    "logout_button": 'svg.lucide-log-out',
}

# Selectores de navegación
NAVIGATION_SELECTORS = {
    "logout_icon": 'svg.lucide-log-out',
    "deposit_arrow": 'svg.arrow-up',
    "menu_toggle": 'button.menu-toggle',
}

# Selectores de operaciones
OPERATION_SELECTORS = {
    "general":{
        "expand_windows": "span#expand-layout",
        "more_options": "p#view-more-less-options",
        "limit_input": "input#limit-input",
        "limit_button": "button[value='limite']",
    },
    "BUY": {
        "button": "button#BUY",
        "amount_input": "input#investment-amount-buy",
        "message": "Compra"
    },
    "SELL": {
        "button": "button#SELL",
        "amount_input": "input#investment-amount-sell",
        "message": "Venta"
    },
    "confirm_buttons": {
        "review_buy": "button#review-buy-button",
        "confirm": "button#order-confirm-button",
    },
}

ORDER_SELECTORS = {
    "orders_list": "div._movementsRows_umu6l_29 div._rowContainer_1m8d2_23",
    "order_row": "div._movementsRows_umu6l_29 div[data-order-id='{}']",
    "cancel_button": "button:has-text('Cancelar orden')",
}


# Selectores comunes
COMMON_SELECTORS = {
    "search_input": "input#input-search",
    "continue_button": 'button:has-text("Continuar")',
    "loading_spinner": ".loading-spinner",
}

# Selectores de búsqueda y lista
LIST_SELECTORS = {
    "search_list": "ul.MuiList-root.search-list",
    "list_item": lambda ticker: f"ul.MuiList-root.search-list li:has(div:has(p:text-is('{ticker}')))",
}

# Selectores de transferencias
TRANSFER_SELECTORS = {
    "withdraw_button": 'div.extraer.clickable-xl',
    "currency_ars": 'label[for="radio-1"]',
    "currency_usd": 'label[for="radio-2"]',
    "amount_input": 'input[type="text"]._input_vr7b7_23',
    "continue_button": 'div._wrapper_289lu_23 button:has-text("Continuar"):not([disabled])'
}

# Selectores de errores y mensajes
MESSAGE_SELECTORS = {
    "error_message": ".error-message",
    "success_message": ".success-message",
    "confirmation_dialog": ".confirmation-dialog",
}

# Selectores de portafolio
PORTFOLIO_SELECTORS = {
    "total_balance": ".total-balance",
    "portfolio_table": "table.portfolio-table",
    "portfolio_item": lambda ticker: f"tr[data-ticker='{ticker}']",
}