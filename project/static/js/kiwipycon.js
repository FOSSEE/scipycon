$(function() {

    // Message ################################################################ 

    var message = $.cookie("message");
    
    if (message != null) { 
        $.jGrowl(message);
        $.cookie("message", null, { path: '/' });
    };
});
