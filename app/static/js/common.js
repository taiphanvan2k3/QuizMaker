const CommonModule = {
    UpdateUrl: function (currentUrl, params) {
        console.log(params);
        let url = new URL(currentUrl);
        for (let key in params) {
            url.searchParams.set(key, params[key]);
        }
        history.replaceState({}, "", url);
    },
};
