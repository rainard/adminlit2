/**
 * Created by eirc on 2017/7/10.
 */


// $(document).ajaxStart(function () {
//     Pace.restart();
//
// });

function load_info(url) {
    $.ajax({
        url: 'static/home/loading.html',
        success: function (result, status) {
            $('.ajax-content').html(result);
            load_content_ajax(url)
        }
    });
}

function load_content(url,content) {
    load_content_ajax(url,content);
}

function load_content_ajax(url, content) {
    $.ajax({
        url: url,
        beforeSend: function () {
            //load_info('static/home/loading.html');
        },
        success: function (result, status) {
            if (content) {
                $(content).delay(1500).html(result)
            } else {
                $('.ajax-content').delay(1500).html(result)
            }
        },
        error: function (resp, p2) {
            try {
                if (resp.status == 403) {
                    $.messager.popup("权限不足");
                    load_info('static/home/403.html');
                }
                if (resp.status == 500) {
                    $.messager.popup("错误页面");
                    load_info('static/home/500.html');
                }
            } catch (ex) {
                console.log(ex)
            }


        }
    })
}


var loading_message = '<div class="shaft-load3">' +
    '                    <div class="shaft1"></div>' +
    '                    <div class="shaft2"></div>' +
    '                    <div class="shaft3"></div>' +
    '                    <div class="shaft4"></div>' +
    '                    <div class="shaft5"></div>' +
    '                    <div class="shaft6"></div>' +
    '                    <div class="shaft7"></div>' +
    '                    <div class="shaft8"></div>' +
    '                    <div class="shaft9"></div>' +
    '                    <div class="shaft10"></div>' +
    '                </div>';

var loading_css = {
    padding: 0,
    margin: 0,
    width: '30%',
    top: '40%',
    left: '35%',
    textAlign: 'center',
    color: '#b5d6e8',
    backgroundColor: "rgba(125,125,125,0)",
    cursor: 'wait',
    border: 'none'
};

$(document).ready(function () {
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
    });


    $.ajaxSetup({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
    });
    $(document).ajaxStart(function () {
        $.blockUI({
            message: loading_message,
            css: loading_css
        });
    });
    $(document).ajaxStop(function () {
        $.unblockUI({fadeOut: 200});
    });
    $("#loginwrap").hide();
    $(".modify-password").click(function () {
        modify_form = $("#loginwrap");
        $('#loginform')[0].reset();
        modify_form.show();
        modify_form.dialog({
            title: "修改密码"
            , 'class': "mydialog"
            , onClose: function () {
                $(this).dialog("close");
                modify_form.hide();
            }
            , buttons: {
                "提交": function () {
                    var me = this;
                    var form = $('#loginform').serializeArray();
                    var data = {};
                    $.each(form, function () {
                        try {
                            data[this.name] = this.value;
                        } catch (ex) {
                            console.log(ex)
                        }
                    });
                    $.ajax({
                        url: '{{ tpl_obj.modify_url }}',
                        data: data,
                        type: 'POST',
                        success: function (result, status) {
                            jsong_obj = $.parseJSON(result);
                            $.messager.popup(jsong_obj.msg);
                            console.log(jsong_obj);
                            if (jsong_obj.success) {
                                setTimeout(function () {
                                        $(window.location).attr('href', '{{ tpl_obj.logout_url }}');
                                    },
                                    3000);

                            }
                        },
                        error: function (result) {
                            if (result.status == 403) {
                                $.messager.popup("权限不足");
                            } else
                                $.messager.popup("操作失败");

                            $(this).dialog("close");
                            modify_form.hide();
                        }
                    });


                }, "关闭": function () {
                    $(this).dialog("close");
                    modify_form.hide();
                }
            }
        });
    });

});