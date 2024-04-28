$(document).ready(function () {
    LayoutModule.init();
    LayoutModule.initEvents();
});

var LayoutModule = (function () {
    var init = function () {
        var userInfoString = Cookies.get("user_info");
        try {
            if (userInfoString) {
                // Decode URI và replace các escape không cần thiết
                var formattedUserInfoString = decodeURIComponent(userInfoString)
                    .replace(/\\054/g, ",")
                    .replace(/\\/g, "");
                userInfo = JSON.parse(formattedUserInfoString);
            } else {
                userInfo = {
                    email: "Guest",
                    picture: "/static/images/default_user_img.jpg",
                };
            }
            if (userInfo) {
                $(".btn-profile .avatar").attr("src", userInfo.picture);
                $("#user-email").text(userInfo.email);
            }
        } catch (error) {
            console.error("Error parsing user info:", error);
            $(".btn-profile .avatar").attr("src", "/static/images/default_user_img.jpg");
            $("#user-email").text("Guest");
        }
        var loggedIn = Cookies.get("user_info"); // Kiểm tra cookie người dùng
        if (loggedIn) {
            $("#login").hide(); // Ẩn Đăng nhập
            $("#profile").show();
            $("#logout").show();
        } else {
            $("#login").show();
            $("#profile").hide();
            $("#logout").hide();
        }
    };

    var initEvents = function () {};

    return {
        init: init,
        initEvents: initEvents,
    };
})();
