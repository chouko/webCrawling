

/**
 * 数字滚动
 * @param {Object} num         开始值
 * @param {Object} maxNum    最大值,最终展示的值
 */
function numRunFun(obj,num,maxNum,speed){
    var numText = num;
    var golb; // 为了清除requestAnimationFrame
    function numSlideFun(){
        numText+=speed; // 速度的计算可以为小数
        if(numText >= maxNum){
            numText = maxNum;
            cancelAnimationFrame(golb);
        }else {
            golb = requestAnimationFrame(numSlideFun);
        }
        obj.innerHTML = ~~(numText)

    }
    numSlideFun();
}

function back(){
    window.history.back();
}

$(".address img").on("touchstart", back)


/*导航栏的切换*/
function showNavbar(e) {

    if ($("#navbar")[0].style.right == '0px') {
        $("#navbar")[0].style.right = '-7.5rem'
    } else {
        $("#navbar")[0].style.right = '0'
    }

}

function showNavli(e) {
    var e = window.event || e;
    if (e.stopPropagation) e.stopPropagation();
    else e.cancelBubble = true;
    $(this).next().toggle()
    if ($(this).next()[0].style.display == "none") {
        $(this).attr('src', './img/jia.png')

    } else {
        $(this).attr('src', './img/jian.png')
    }

}



function stop() {
    var e = window.event || e;
    if (e.stopPropagation) e.stopPropagation();
    else e.cancelBubble = true;

}

function showMenus(e){

    $("#menu_list").toggle()

}

$(".details>a").each(function (i) {
    $(this)[0].addEventListener('click',function(e){
        $(this).parent().next().toggle()

    })
})


$("#down_menu").on("touchstart", showMenus)
$(".menus li a").on("touchstart", stop)
$(".nav img").on("touchstart", showNavli)
$(".classify li").on("click", showNavbar)
$("#navbar").on("touchstart", showNavbar)
$("#navbar a").on("touchstart", stop)
$("#menu_pic").on("touchstart", showNavbar)
$(".list_footer img").on("touchstart", showNavli)

$('#captchaImg').click(function() {
    $(this).attr('src', '/captcha/getCaptchaCode.jpg');
});
// $("#phone").blur(function(){
//     var phone = $("#phone").val();
//     if(phone=="")  return;
//     isPhone(phone);
// });
function isPhone(phone){
    var RegCellPhone = /^(1)([0-9]{10})?$/;
    var  falg=phone.search(RegCellPhone);
    if (falg==-1){
        alert("手机号不正确");
        this.focus();
    }
}
function  form() {
    var name = $("#name").val();
    var sex = $("input[name='sex']").next(".active").html();
    var level = $("input[name='level']").next(".active").html();
    var experience =$("input[name='experience']").next(".active").html();
    var assets =$("input[name='assets']").next(".active").html();
    var ability = $("input[name='ability']").next(".active").html();
    var age = $("#age").val();
    var background = $("#background").val();
    var phone = $("#phone").val();
    var wx = $("#wx").val();
    var textcontent = $("#textcontent").val();
    var code = $("#code").val();
    if(!phone && !wx){

        alert("请输入联系方式");
    }else{
        var data={
            name:name,
            sex:sex,
            level:level,
            experience:experience,
            assets:assets,
            ability:ability,
            age:age,
            background:background,
            wx:wx,
            phone:phone,
            message:textcontent,
            code:code
        }
        $.ajax({
            type: "post",
            url: "/leavingMessage/add",
            data: data,
            async: true,
            success: function (data) {
                console.log(data)
                if(data.code==400){
                    alert("验证码错误");
                }
                if(data.code==200){
                    alert("感谢您选择中加国际，我们的工作人员将会在24小时内联系您，与您探讨您的相关问题")
                    $("#name").val("");
                    $("#phone").val("");
                    $("#textcontent").val("");
                    $("#code").val("");
                    $("#age").val("");
                    $("#background").val("");
                    $("#wx").val("");
                    $("input[name='sex']").next(".active").removeClass("active");
                    $("input[name='level']").next(".active").removeClass("active");
                    $("input[name='experience']").next(".active").removeClass("active");
                    $("input[name='assets']").next(".active").removeClass("active");
                    $("input[name='ability']").next(".active").removeClass("active");
                }
            }
        })
    }

}

/*导航条控制*/
function goIndex(){
    //跳转首页
    window.location.href="/"
    sessionStorage.setItem('firstactive', 0)//设置缓存为0

}
$("#ul_nav>li").each(function (i) {
    $(this)[0].addEventListener('click',function(e){
        sessionStorage.setItem('firstactive', i)

    })
})
$("#ul_nav>li")[sessionStorage.getItem('firstactive') || 0].className='actived'
var eleList = document.querySelectorAll('.classify')

for (var i = 0; i < eleList.length; i++) {
    eleList[i].addEventListener('click',function(e){
        var _child = e.target.parentNode.parentNode.children
        for (var j = 0; j < _child.length; j++) {
            if (_child[j] == e.target.parentNode) {
                sessionStorage.setItem('_active', j)
            }
        }
    })
}
$("#ul_nav>li .classify")[sessionStorage.getItem('firstactive') || 0].children[sessionStorage.getItem('_active')].className = 'actived'



