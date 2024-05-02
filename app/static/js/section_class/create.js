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
    };

    const InitEvents = function () {
        window.addEventListener("scroll", HandleScroll);

        $(".btn-add").on("click", function () {
            HandleAddVocabBlock();
        });

        $(".btn-delete").on("click", function () {
            HandleDeleteVocabBlock($(this));
        });
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

    return {
        Init: Init,
        InitEvents: InitEvents,
    };
})();
