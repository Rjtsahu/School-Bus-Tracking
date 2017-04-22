// some common constants
 var TOAST_TIME=5000;
$(document).ready(function() {
    initials();
  });

function my_modal(id,name,email,title,message,date,time) {
    // set these values to modal
    $('#mod-title').text(title);
    $('#mod-other-data').text('By:'+name+' on '+time+' date: '+date);
    $('#mod-detail').text(message);
    $('#mod-date').text(date);
    $('#mod-time').text(time);
    $('#mod-reply-but').attr('onclick','my_modal_reply(\''+id+'\',\''+email+'\');');
    $('#modal1').modal('open');
}
function my_modal_reply(msg_id,email) {
    //send email
    var title=$('#mod-input-title').val();
    var msg=$('#mod-input-message').val();
    message={msg_id:msg_id,email:email,title:title,message:msg};
    console.log(message);
    $.post( "/admin/api/reply_email",message);
    $('#modal1').modal('close');
    // show success toast
     Materialize.toast('Reply message sent !!!', TOAST_TIME);
}

function initials() {
    Materialize.updateTextFields();
	$('.modal').modal();
	$(".button-collapse").sideNav();
   $('select').material_select();
    // set default option
   $('.bus:nth-child(1)').prop('selected', true);
}