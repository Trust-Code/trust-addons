(function() {
    var instance = openerp;
    instance.web.logout = function() {
	var Users = new instance.Model('res.users');
	Users.call('logout_user').then(function(result) {
	    instance.web.redirect('/web/session/logout');
	});
    };
})();