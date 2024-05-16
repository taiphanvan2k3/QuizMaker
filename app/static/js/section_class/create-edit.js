$(document).ready(function () {
    CreateEditSectionClassModule.Init();
    CreateEditSectionClassModule.InitEvents();
});

const CreateEditSectionClassModule = (function () {
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

        $(window).on("scroll", function () {
            if (window.scrollY >= 100) {
                $(".main-content>.header").addClass("fixed");
            } else {
                $(".main-content>.header").removeClass("fixed");
            }
        });

        $(document)
            .on("input", ".autocomplete-input-en", function () {
                const query = $(this).text();
                const $suggestionsList = $(this)
                    .closest(".vocab-info")
                    .find(".suggestions-list-en");
                if (query.length === 0) {
                    $suggestionsList.empty();
                    return;
                }
                GetSuggestionsEn(query, $suggestionsList);
            })
            .on("focusout", ".autocomplete-input-en", function () {
                const $input = $(this);
                setTimeout(function () {
                    if (!$input.is(":focus")) {
                        $input
                            .closest(".vocab-info")
                            .find(".suggestions-list-en")
                            .empty();
                    }
                }, 300);
            });

        $(document)
            .on("input", ".autocomplete-input-vi", function () {
                const query = $(this)
                    .closest(".vocab-info")
                    .find(".autocomplete-input-en")
                    .text();
                const $suggestionsList = $(this)
                    .closest(".vocab-info")
                    .find(".suggestions-list-vi");
                if (query.length === 0) {
                    $suggestionsList.empty();
                    return;
                }
                GetSuggestionsVi(query, $suggestionsList);
            })
            .on("focusout", ".autocomplete-input-vi", function () {
                const $input = $(this);
                setTimeout(function () {
                    if (!$input.is(":focus")) {
                        $input
                            .closest(".vocab-info")
                            .find(".suggestions-list-vi")
                            .empty();
                    }
                }, 300);
            });

        $(document).on("click", ".suggestions-list-en .clickable", function () {
            const selectedText = $(this).text();
            const selectedIndex = $(this).data("index");
            console.log(
                `Clicked on ${selectedText} with index ${selectedIndex}`
            );
            $(this)
                .closest(".vocab-info")
                .find(".autocomplete-input-en")
                .text(selectedText);
            $(this).closest(".vocab-info").find(".suggestions-list-en").empty();
        });

        $(document).on("click", ".suggestions-list-vi .clickable", function () {
            const selectedText = $(this).text();
            const selectedIndex = $(this).data("index");
            console.log(
                `Clicked on ${selectedText} with index ${selectedIndex}`
            );
            $(this)
                .closest(".vocab-info")
                .find(".autocomplete-input-vi")
                .text(selectedText);
            $(this).closest(".vocab-info").find(".suggestions-list-vi").empty();
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

            $(".vocab-list .vocab-info").each(function (index) {
                data.vocabularies.push({
                    id: $(this).data("id") == 0 ? index : $(this).data("id"),
                    english_text: $(this).find(".english-text").text(),
                    vietnamese_text: $(this).find(".vietnamese-text").text(),
                    order: index + 1,
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
            const sectionClassId = $("#section-class-id").val();
            let data = GetData();
            let isEdit = false;
            if (sectionClassId != "0") {
                data = {
                    id: sectionClassId,
                    ...data,
                };
                isEdit = true;
            }

            $.ajax({
                url: isEdit ? urls.edit : urls.create,
                type: "POST",
                dataType: "json",
                data: data,
                success: function (response) {
                    console.log("Response", response);
                    if (response.code === 200) {
                        if (isEdit) {
                            CommonModule.ShowToast(
                                "success",
                                "Lưu thành công."
                            );
                        } else {
                            CommonModule.ShowModal(
                                POP_UP_TYPE.SUCCESS,
                                "Thành công",
                                "Đã tạo mới thành công lớp học tập",
                                function () {
                                    window.location.href =
                                        urls.list_of_section_class_page;
                                }
                            );
                        }
                    } else {
                        CommonModule.ShowModal(
                            POP_UP_TYPE.ERROR,
                            "Có lỗi xảy ra",
                            response.message
                        );
                    }
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

    /**
     * Get suggestions from server for autocomplete english text
     * Author: ManhTD, created at 2024/05/11
     */
    const GetSuggestionsEn = function (query, $suggestionsList) {
        try {
            $.ajax({
                url: `/section_class/autocomplete_en?query=${encodeURIComponent(
                    query
                )}`,
                type: "GET",
                dataType: "json",
                success: function (response) {
                    $suggestionsList.empty();
                    if (response.code === 200) {
                        response.data
                            .slice(0, 5)
                            .forEach(function (result, index) {
                                const li = $("<li>")
                                    .addClass(
                                        "clickable list-group-item list-group-item-action"
                                    )
                                    .attr("data-index", index)
                                    .text(result);
                                $suggestionsList.append(li);
                            });
                    }
                },
                error: function (error) {
                    console.log("Error fetching suggestions: ", error);
                },
                complete: function () {
                    CommonModule.SetLoading(false);
                },
            });
        } catch (error) {
            console.log("GetSuggestionsEn Error", error);
        }
    };

    /**
     * Get suggestions from server for autocomplete vietnamese text
     * Author: ManhTD, created at 2024/05/11
     */
    const GetSuggestionsVi = function (query, $suggestionsList) {
        try {
            $.ajax({
                url: `/section_class/autocomplete_vi?query=${encodeURIComponent(
                    query
                )}`,
                type: "GET",
                dataType: "json",
                success: function (response) {
                    $suggestionsList.empty();
                    if (response.code === 200) {
                        response.data.forEach(function (result, index) {
                            const li = $("<li>")
                                .addClass(
                                    "clickable list-group-item list-group-item-action"
                                )
                                .attr("data-index", index)
                                .text(result);
                            $suggestionsList.append(li);
                        });
                    }
                },
                error: function (error) {
                    console.log("Error fetching suggestions: ", error);
                },
                complete: function () {
                    CommonModule.SetLoading(false);
                },
            });
        } catch (error) {
            console.log("GetSuggestionsEn Error", error);
        }
    };

    return {
        Init: Init,
        InitEvents: InitEvents,
    };
})();
