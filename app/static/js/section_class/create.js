$(document).ready(function () {
    AddSectionClassModule.Init();
    AddSectionClassModule.InitEvents();
});

const AddSectionClassModule = (function () {
    let vocabBlockQuantity = 5;

    const vocabList = document.querySelector(".vocab-list");
    let observer = null;

    const mutationCallback = (entries) => {
        entries.forEach((entry) => {
            // Khi trong vocabList có add thêm element mới thì observer biết được các element được add là những node
            // nào và thực hiện animation cho chúng
            entry.addedNodes.forEach((newNode) => {
                AnimateNewNode(newNode);
            });
        });
    };

    const Init = function () {
        CommonModule.SetDefaultAjax();

        // Init observer
        observer = new MutationObserver(mutationCallback);
        observer.observe(vocabList, {
            attributes: false,
            characterData: false,
            childList: true,
            subtree: false,
        });

        // Init tooltip bootstrap
        const tooltipTriggerList = document.querySelectorAll(
            '[data-bs-toggle="tooltip"]'
        );
        [...tooltipTriggerList].map(
            (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
        );

        InitTabIndex();
    };

    const InitEvents = function () {
        window.addEventListener("scroll", HandleScroll);

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

    const HandleScroll = function () {
        try {
            if (window.scrollY > 100) {
                $(".main-content > .header").addClass("fixed");
            } else {
                $(".main-content > .header").removeClass("fixed");
            }
        } catch (error) {
            console.log("HandleScroll", error);
        }
    };

    const HandleAddVocabBlock = function () {
        try {
            const vocabBlockTemplate = $(".vocab-block-template").html();
            const newElement = $(vocabBlockTemplate)[0];
            vocabList.appendChild(newElement);
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
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: "smooth", // Optional: scroll behavior
            });

            const newElement = $(ele);
            vocabBlockQuantity++;
            newElement.find(".stt").text(vocabBlockQuantity);
            newElement.find(".btn-drag").tooltip();
            newElement.find(".btn-delete").tooltip();
            newElement.find(".btn-delete").on("click", function () {
                HandleDeleteVocabBlock($(this));
            });
            newElement.find(".english-text").focus();
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
