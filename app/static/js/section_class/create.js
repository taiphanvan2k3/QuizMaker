$(document).ready(function () {
    AddSectionClassModule.Init();
    AddSectionClassModule.InitEvents();
});

const AddSectionClassModule = (function () {
    let vocabBlockQuantity = 5;
    const vocabList = document.querySelector(".vocab-list");

    const Init = function () {
        CommonModule.SetDefaultAjax();

        // Init tooltip bootstrap
        const tooltipTriggerList = document.querySelectorAll(
            '[data-bs-toggle="tooltip"]'
        );
        [...tooltipTriggerList].map(
            (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
        );

        InitTabIndex();
        $(".vocab-list").sortable({
            scroll: false, // Vô hiệu hóa cuộn
            tolerance: "pointer", // Xác định vị trí con trỏ chuột
            cancel: ".input",
            handle: ".btn-drag",
        });
    };

    const InitEvents = function () {
        $(".btn-add").on("click", function () {
            HandleAddVocabBlock();
        });

        $(".btn-delete").on("click", function () {
            HandleDeleteVocabBlock($(this));
        });

        $(".btn-create").on("click", function () {
            HandleSubmit();
        });

        // Bắt sự kiện ctrl S
        $(document).on("keydown", function (e) {
            if (e.ctrlKey && e.key === "s") {
                e.preventDefault();
                HandleSubmit();
            }
        });
    };

    const InitTabIndex = function () {
        try {
            $("input:not([type='checkbox']), .input, textarea").each(function (
                index
            ) {
                $(this).attr("tabindex", index + 1);
            });
        } catch (error) {
            console.log("InitTabIndex", error);
        }
    };

    const HandleAddVocabBlock = function () {
        try {
            const vocabBlockTemplate = $(".vocab-block-template").html();
            const newElement = $(vocabBlockTemplate)[0];
            vocabList.appendChild(newElement);
            AnimateNewNode(newElement);
        } catch (error) {
            console.log("HandleAddVocabBlock", error);
        }
    };

    const HandleDeleteVocabBlock = function ($btnDelete) {
        try {
            const vocabBlock = $btnDelete.closest(".vocab-block");
            $btnDelete.tooltip("hide");
            AnimateRemovedNode(vocabBlock[0]);
        } catch (error) {
            console.log("HandleDeleteVocabBlock", error);
        }
    };

    /**
     * Make animation when add a element
     * Author: TaiPV, created at 2024/05/03
     */
    const AnimateNewNode = (ele) => {
        ele.animate(
            [
                {
                    height: "0px",
                    opacity: 0,
                },
                {
                    height: `${ele.scrollHeight}px`,
                    opacity: 1,
                },
            ],
            {
                duration: 400,
            }
        ).addEventListener("finish", () => {
            console.log("Scroll to bottom");

            const newElement = $(ele);
            vocabBlockQuantity++;
            newElement.find(".btn-drag").tooltip();
            newElement.find(".btn-delete").tooltip();
            newElement.find(".btn-delete").on("click", function () {
                HandleDeleteVocabBlock($(this));
            });
            newElement.find(".english-text").focus();

            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: "smooth", // Optional: scroll behavior
            });
        });
    };

    /**
     * Make animation when remove a element
     * Author: TaiPV, created at 2024/05/03
     */
    const AnimateRemovedNode = (ele) => {
        ele.animate(
            [
                {
                    height: `${ele.scrollHeight}px`,
                    opacity: 1,
                },
                {
                    height: "0px",
                    opacity: 0,
                },
            ],
            {
                duration: 300,
                easing: "linear",
            }
        ).addEventListener("finish", () => {
            ele.remove();
            vocabBlockQuantity--;
        });
    };

    const GetData = function () {
        try {
            const data = {
                sectionClassName: $("#section-class-name").val(),
                sectionClassDesc: $("#section-class-desc").val(),
                isPublic: $("#is-public").is(":checked"),
                vocabularies: [],
            };

            $(".vocab-list .vocab-info").each(function () {
                data.vocabularies.push({
                    english_text: $(this).find(".english-text").text(),
                    vietnamese_text: $(this).find(".vietnamese-text").text(),
                });
            });

            console.log(data);
            return data;
        } catch (error) {
            console.log("GetData", error);
        }
    };

    const HandleSubmit = function () {
        try {
            $.ajax({
                url: urls.create,
                type: "POST",
                dataType: "json",
                data: GetData(),
                success: function (response) {
                    console.log("Response", response);
                    window.location.href = urls.list_of_section_class_page;
                },
                error: function (error) {
                    console.log("Error", error);
                },
                complete: function () {
                    CommonModule.SetLoading(false);
                },
            });
        } catch (error) {
            console.log("Cannot submit", error);
        }
    };

    return {
        Init: Init,
        InitEvents: InitEvents,
    };
})();
