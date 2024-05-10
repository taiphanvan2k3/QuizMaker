const CommonModule = {
    UpdateUrl: function (currentUrl, params) {
        console.log(params);
        let url = new URL(currentUrl);
        for (let key in params) {
            url.searchParams.set(key, params[key]);
        }
        history.replaceState({}, "", url);
    },
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
                }
                module.SetLoading(true);
            },
        });
    },
    SetLoading: function (isLoading) {
        if (isLoading) {
            $("#loading-icon")?.show();
        } else {
            $("#loading-icon")?.hide();
        }
    },
};
