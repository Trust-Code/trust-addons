openerp.trust_my_task = function(openerp) {
    openerp.web_kanban.KanbanView.include({
        events: {
            'click a.oe_my_task': function (e) {
                alert('oi');
                e.stopPropagation();
            }
        },
    });
};
