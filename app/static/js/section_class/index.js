$(document).ready(function () {
    ListOfSectionClassModule.InitEvents();
});

const ListOfSectionClassModule = (function () {
    const InitEvents = function () {
        $(".dropdown-item").on("click", function () {
            ChangeSectionTypes($(this).data("val"));
        });

        $(".section-item").on("click", function () {
            console.log($(this).attr("id"));
        });
    };

    const ChangeSectionTypes = function (sectionType) {
        try {
            $.ajax({
                url: urls.sectionClassList,
                type: "POST",
                dataType: "json",
                data: {
                    sectionType: sectionType,
                },
                success: function (res) {
                    if (res.code === 200) {
                        CommonModule.UpdateUrl(window.location.href, {
                            sectionType,
                        });

                        if (sectionType == "all") {
                            $(".dropdown-toggle").text("Tất cả");
                        } else {
                            $(".dropdown-toggle").text("Tự tạo");
                        }
                        $("#section-list").html(res.html);
                    } else {
                        console.log("ChangeSectionTypes error: ", res.message);
                    }
                },
                error: function (error) {
                    console.log("ChangeSectionTypes: ", error.message);
                },
            });
        } catch (error) {
            console.log("ChangeSectionTypes: ", error.message);
        }
    };

    return {
        InitEvents: InitEvents,
    };
})();
