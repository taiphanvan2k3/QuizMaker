const POP_UP_TYPE = {
    SUCCESS: "success",
    ERROR: "error",
};

const CommonModule = {
    /**
     * Thay đổi URL hiện tại của trang mà không gây reload trang
     *
     * Author: TaiPV, created at 28/04/2024
     * @param {string} currentUrl: url hiện tại
     * @param {string} params: object chứa các tham số cần thêm vào url
     */
    UpdateUrl: function (currentUrl, params) {
        console.log(params);
        let url = new URL(currentUrl);
        for (let key in params) {
            url.searchParams.set(key, params[key]);
        }
        history.replaceState({}, "", url);
    },

    /**
     * Hàm thiết lập các options mặc định cho 1 request khi sử dụng Ajax
     *
     * Author: TaiPV, created at 11/05/2024
     */
    SetDefaultAjax: function () {
        const module = this;
        $.ajaxSetup({
            contentType: "application/json", // Thiết lập header Content-Type là application/json
            processData: false, // Vô hiệu hóa xử lý dữ liệu trước khi gửi
            beforeSend: function (jqXHR, options) {
                if (
                    options.contentType == "application/json" &&
                    typeof options.data != "string"
                ) {
                    options.data = JSON.stringify(options.data);
                    console.log(options.data);
                }
                if (options.global && options.type !== "GET") {
                    module.SetLoading(true);
                }
            },
            complete: function () {
                module.SetLoading(false);
            },
        });
    },

    /**
     * Thiết lập hiển thị icon loading
     *
     * Author: TaiPV, created at 11/05/2024
     * @param {boolean} isLoading: true nếu muốn hiển thị icon loading, false nếu muốn ẩn
     */
    SetLoading: function (isLoading) {
        if (isLoading) {
            $("#loading-icon")?.show();
        } else {
            $("#loading-icon")?.hide();
        }
    },

    /**
     * Author: TaiPV, created at 11/05/2024
     *
     * @param {string} popup_type: see POP_UP_TYPE
     * @param {string} title
     * @param {string} message
     * @param {function} callback
     */
    ShowModal: function (popup_type, title, message, callback) {
        $("#ModalToggleLabel").text(title);
        $(".modal-body").text(message);
        if (popup_type === POP_UP_TYPE.SUCCESS) {
            $(".dismiss-btn").text("OK");
            $(".dismiss-btn").on("click", function () {
                if (callback) {
                    callback();
                }
            });
        } else {
            $(".dismiss-btn").text("Đóng");
        }
        $("#btn-show-popup").trigger("click");
    },

    /**
     * Author: TaiPV, created at 14/05/2024
     *
     * @param {string} type: success, error, info, warning
     * @param {string} message: nội dung thông báo
     * @param {object} style: truyền CSS inline để custom style cho toast
     */
    ShowToast: function (type, message, style) {
        let toast;
        if (type == "success") {
            toast = FuiToast.success;
        } else if (type == "error") {
            toast = FuiToast.error;
        } else if (type == "info") {
            toast = FuiToast.info;
        } else {
            toast = FuiToast.warning;
        }
        toast(message, style);
        $(".fui-toast").css(style ?? {});
    },

    /**
     * Làm hiệu ứng tung giấy hoa
     *
     * Author: TaiPV, created at 13/05/2024
     * Library: https://www.kirilv.com/canvas-confetti/
     */
    ConfettiToss: function () {
        const duration = 3 * 1000;
        const animationEnd = Date.now() + duration;
        const defaults = {
            startVelocity: 20,
            spread: 360,
            ticks: 60,
            zIndex: 0,
        };

        function randomInRange(min, max) {
            return Math.random() * (max - min) + min;
        }

        const interval = setInterval(function () {
            const timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) {
                return clearInterval(interval);
            }

            const particleCount = 60 * (timeLeft / duration);

            // since particles fall down, start a bit higher than random
            confetti({
                ...defaults,
                particleCount,
                origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
            });
            confetti({
                ...defaults,
                particleCount,
                origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
            });
        }, 250);
    },

    GetCookie: function (name) {
        let cookieName = name + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let cookies = decodedCookie.split(";");
        console.log(cookies);
        for (let cookie of cookies) {
            if (cookie.trim().startsWith(cookieName)) {
                return cookie.substring(cookieName.length);
            }
        }
    },

    GetTimeDiff: function (date) {
        const now = new Date();
        const diff = now - date;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        const months = Math.floor(days / 30);
        const years = Math.floor(months / 12);
        let timeDiff = "";
        if (days == 0) {
            if (hours == 0) {
                if (minutes == 0) timeDiff = "vài giây trước";
                else timeDiff = `${minutes} phút trước`;
            } else {
                timeDiff = `${hours} giờ trước`;
            }
        } else if (days <= 31) {
            timeDiff = `${days} ngày trước`;
        } else if (months <= 12) {
            timeDiff = `${months} tháng trước`;
        } else {
            timeDiff = `${years} năm trước`;
        }
        return timeDiff;
    },
};
