$(document).ready(function () {
    SectionClassDetailModule.Init();
    SectionClassDetailModule.InitEvents();
});

const SectionClassDetailModule = (function () {
    const sectionClassId = $("#section-class-id").val();

    let currentVocabIndex = 0;
    let originalVocabularies = vocabData;
    let currentVocabularies;
    let vocabCount = vocabData.length;
    let learnedVocabularies = [];
    let learningVocabularies = [];
    const btnChecked = $(".btn-checked");
    const vocabularyItemTemplate = $(".vocabulary-item:first").clone();

    // Lưu trạng thái hành động trước đó
    let previousAction;
    let previousEditedVocabulary;

    // Các option cho việc hiển thị từ vựng
    const viewOptions = {
        orderBy: "original",
        isStared: false,
    };

    const PreprocessingData = function () {
        try {
            originalVocabularies.forEach((vocab, index) => {
                vocab.index = index;
                vocab.url = urls.update.replace("0", vocab.id);
            });
            currentVocabularies = [...originalVocabularies];
        } catch (error) {
            console.log("PreprocessingData: ", error);
        }
    };

    let debounceTimeout;

    const Init = function () {
        const tooltipTriggerList = document.querySelectorAll(
            '[data-bs-toggle="tooltip"]'
        );
        [...tooltipTriggerList].map(
            (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
        );
    };

    const InitEvents = function () {
        PreprocessingData();
        $("#card").on("click", function () {
            $(this).toggleClass("turned");
        });

        $(".btn-x, .btn-checked").on("click", function () {
            HandleNextVocab($(this));
        });

        // Phát âm thanh khi bấm vào loa trên card
        $("#card .btn-speech").on("click", function (e) {
            GetAudioFromText($(this), $(this).data("text"));
            e.stopPropagation();
        });

        $(".btn-revert").prop("disabled", true);
        $(".btn-revert").on("click", HandleRevertVocab);

        $(".review-block").on("click", SetDataForReviewing);
        $(".learn-again-block").on("click", ResetData);

        $(".vocabularies-block .dropdown-item").on("click", function () {
            viewOptions.orderBy = $(this).data("order");
            OrderByVocabularies();
        });

        $(".view-options span").on("click", function () {
            $(".view-options span").removeClass("active");
            $(this).addClass("active");
            viewOptions.isStared = $(this).data("view-option") === "stared";
            OrderByVocabularies();
        });

        // Xử lý edit trên từng vocabulary-item
        $(".vocabulary-item").on("click", function (e) {
            // Nếu vẫn đang click trên element trước đó thì không disable chế độ edit
            // nhưng nếu click ra ngoài hay vào element khác thì disable chế độ edit
            console.log("Vocabulary item click");
            if ($(this)[0] === previousEditedVocabulary?.element[0]) {
                e.stopPropagation();
            }
        });

        $(document).on("click", function () {
            if (previousEditedVocabulary) {
                HandleDisableEdit();
            }
        });

        // Phát âm thanh khi bấm vào load trên vocabulary-item
        $(".vocabulary-item .btn-speech").on("click", function (e) {
            GetAudioFromText($(this), $(this).data("text"));
            e.stopPropagation();
        });

        $(".vocabulary-item .btn-edit").on("click", function (e) {
            // trigger document click event để disable chế độ edit trước đó
            $(document).trigger("click");
            HandleEditVocabulary($(this));
            e.stopPropagation();
        });

        $(".vocabulary-item .btn-star").on("click", function (e) {
            HandleUpdateStar($(this));
            e.stopPropagation();
        });

        $(".menu-item").hover(
            function () {
                $(this).find(".fa-book-copy").addClass("fa-bounce");
            },
            function () {
                $(this).find(".fa-book-copy").removeClass("fa-bounce");
            }
        );

        $(".btn-share").on("click", GetCurrentMembers);

        $("#search-email").on("input", function () {
            SearchUsers($(this));
        });

        $(document).on("click", ".new-user-element", function () {
            $("#search-email").val($(this).find(".email").text());
            $(".suggestion-users").empty();
        });

        $("#sharingModal").on("click", function () {
            $(".suggestion-users").empty();
        });

        $(".btn-submit-share").prop("disabled", true);
        $(".btn-submit-share").on("click", HandleSharingToUser);

        $(".invitation-options button").on("click", function () {
            HandleResponseInvitation($(this));
        });

        $('.do-exam').on("click", function () {
            CheckAndNavigateDoExam();
        });
    };

    const HandleNextVocab = function ($btn) {
        try {
            if ($btn.prop("disabled") || currentVocabIndex == vocabCount) {
                return;
            }

            $(".btn-revert").prop("disabled", false);
            if ($btn[0] == btnChecked[0]) {
                learnedVocabularies.push(
                    currentVocabularies[currentVocabIndex]
                );
            } else {
                learningVocabularies.push(
                    currentVocabularies[currentVocabIndex]
                );
            }

            if (currentVocabIndex + 1 < vocabCount) {
                const vocab = currentVocabularies[currentVocabIndex + 1];
                $(".front p").text(vocab.english);
                $(".back p").text(vocab.vietnamese);
                $("#card .btn-speech").data("text", vocab.english);
                if ($("#is-auto-audio").is(":checked")) {
                    GetAudioFromText($("#card .btn-speech"), vocab.english);
                }
            }
            currentVocabIndex++;
            UpdateProgressBar();

            $(".counter").text(`${currentVocabIndex + 1} / ${vocabCount}`);
            if (currentVocabIndex === vocabCount - 1) {
                $btn.prop("disabled", true);
            }

            let message = ".learned-message";
            if ($btn[0] == btnChecked[0]) {
                $(".learned-message").addClass("active");
                previousAction = "learned";
            } else {
                $(".learning-message").addClass("active");
                message = ".learning-message";
                previousAction = "learning";
            }
            $btn.prop("disabled", true);

            const currentHTML = $btn.html();
            $btn.text(
                $btn[0] == btnChecked[0]
                    ? learnedVocabularies.length
                    : learningVocabularies.length
            );
            setTimeout(function () {
                $(message).removeClass("active");
                $btn.prop("disabled", false);
                $btn.html(currentHTML);
            }, 300);

            if (currentVocabIndex == vocabCount) {
                $(".flash-card-block").addClass("dis-none");
                $("#achievement").removeClass("dis-none");
                $(".learned-vocab .qty").text(learnedVocabularies.length);
                $(".learning-vocab .qty").text(learningVocabularies.length);
                CommonModule.ConfettiToss();
                if (learningVocabularies.length == 0) {
                    $(".review-block").removeClass("d-flex").addClass("d-none");
                }
            }
        } catch (error) {
            console.log("HandleNextVocab: ", error);
        }
    };

    /**
     * Xử lý sự kiện revert lại từ vựng trước đó
     * Author: TaiPV, created at 12/05/2024
     */
    const HandleRevertVocab = function () {
        try {
            if (currentVocabIndex == 0) return;
            currentVocabIndex--;
            UpdateProgressBar();

            const vocab = currentVocabularies[currentVocabIndex];

            $(".revert-message").addClass("active");
            $(".revert-message p").text(vocab.english);

            setTimeout(function () {
                $(".revert-message").removeClass("active");
            }, 300);

            $(".front p").text(vocab.english);
            $(".back p").text(vocab.vietnamese);
            $(".btn-speech").data("text", vocab.english);
            $(".counter").text(`${currentVocabIndex + 1} / ${vocabCount}`);

            if (currentVocabIndex === 0) {
                $(".btn-revert").prop("disabled", true);
            }

            // Revert lại giá trị của learnedVocabularies và learningVocabularies
            if (previousAction === "learned") {
                learnedVocabularies.pop();
            } else {
                learningVocabularies.pop();
            }
        } catch (error) {
            console.log("HandleRevertVocab: ", error);
        }
    };

    /**
     * Sử dụng API SpeechSynthesisUtterance để chuyển đổi text thành audio
     * Author: TaiPV, created at 12/05/2024
     */
    const GetAudioFromText = function ($btn, text) {
        try {
            console.log($btn);
            $btn.addClass("active");
            const audio = new SpeechSynthesisUtterance(text);
            audio.lang = "en-US";
            audio.voice = window.speechSynthesis.getVoices()[5];
            window.speechSynthesis.speak(audio);
            audio.onend = function () {
                $btn.removeClass("active");
            };
        } catch (error) {
            console.log("GetAudioFromText: ", error);
        }
    };

    /**
     * Reset lại dữ liệu flash card ban đầu
     * Author: TaiPV, created at 12/05/2024
     */
    const ResetData = function () {
        console.log(originalVocabularies);
        currentVocabularies = [...originalVocabularies];
        vocabCount = currentVocabularies.length;
        currentVocabIndex = 0;
        learnedVocabularies.length = 0;
        learningVocabularies.length = 0;
        $(".front p").text(currentVocabularies[currentVocabIndex].english);
        $(".back p").text(currentVocabularies[currentVocabIndex].vietnamese);
        $(".btn-speech").data(
            "text",
            currentVocabularies[currentVocabIndex].english
        );
        $(".counter").text(`${currentVocabIndex + 1} / ${vocabCount}`);
        $(".btn-revert").prop("disabled", true);
        $(".flash-card-block").removeClass("dis-none");
        $("#achievement").addClass("dis-none");
        $(".review-block").addClass("d-flex").removeClass("d-none");
        UpdateProgressBar();
    };

    /**
     * Set dữ liệu cho việc ôn tập lại các từ vựng đang học
     * Author: TaiPV, created at 12/05/2024
     */
    const SetDataForReviewing = function () {
        currentVocabularies = [...learningVocabularies];
        vocabCount = currentVocabularies.length;
        currentVocabIndex = 0;
        learnedVocabularies.length = 0;
        learningVocabularies.length = 0;
        $(".front p").text(currentVocabularies[currentVocabIndex].english);
        $(".back p").text(currentVocabularies[currentVocabIndex].vietnamese);
        $(".btn-speech").data(
            "text",
            currentVocabularies[currentVocabIndex].english
        );
        $(".counter").text(`${currentVocabIndex + 1} / ${vocabCount}`);
        $(".btn-revert").prop("disabled", true);
        $(".flash-card-block").removeClass("dis-none");
        $("#achievement").addClass("dis-none");
        UpdateProgressBar();
    };

    const UpdateProgressBar = function () {
        try {
            const percent = (currentVocabIndex / vocabCount) * 100;
            $(".horizontal-divider .progress-bar").css("width", `${percent}%`);
        } catch (error) {
            console.log("UpdateProgressBar: ", error);
        }
    };

    const OrderByVocabularies = function () {
        try {
            let data = [...originalVocabularies];
            if (viewOptions.isStared) {
                data = data.filter(
                    (vocab) => vocab.is_stared === viewOptions.isStared
                );
            }

            if (viewOptions.orderBy === "dictionary") {
                data.sort((a, b) => a.english.localeCompare(b.english));
                $("#btn-dropdown").text("Bảng chữ cái");
            } else {
                $("#btn-dropdown").text("Thứ tự gốc");
            }

            const wrapper = $(".vocabularies-block .wrapper");

            wrapper.empty();

            data.forEach((vocab) => {
                const vocabElement = vocabularyItemTemplate.clone();
                vocabElement
                    .find(".english-text")
                    .text(vocab.english)
                    .data("old_value", vocab.english);

                vocabElement
                    .find(".vietnamese-text")
                    .text(vocab.vietnamese)
                    .data("old_value", vocab.vietnamese);

                vocabElement.find(".btn-speech").data("text", vocab.english);
                vocabElement.find(".btn-star").data("index", vocab.index);
                vocabElement.find(".btn-star").data("url", vocab.url);
                vocabElement.find(".btn-edit").data("url", vocab.url);
                vocabElement
                    .find(".btn-star")
                    .toggleClass("active", vocab.is_stared);

                // Add lại event click cho từng vocabulary-item
                vocabElement.find(".btn-speech").on("click", function (e) {
                    GetAudioFromText($(this), $(this).data("text"));
                    e.stopPropagation();
                });
                vocabElement.find(".btn-edit").on("click", function (e) {
                    HandleEditVocabulary($(this));
                    e.stopPropagation();
                });
                vocabElement.find(".btn-star").on("click", function (e) {
                    HandleUpdateStar($(this));
                    e.stopPropagation();
                });
                wrapper.append(vocabElement);
            });
        } catch (error) {
            console.log("OrderByVocabularies: ", error);
        }
    };

    /**
     * Xử lý event khi nhấn vào nút edit trên từng từ vựng
     *
     * Author: TaiPV, created at 13/05/2024
     */
    const HandleEditVocabulary = function ($btnEdit) {
        try {
            const vocabElement = $btnEdit.closest(".vocabulary-item");
            vocabElement
                .find(".english-text")
                .attr("contenteditable", true)
                .addClass("active");
            vocabElement
                .find(".vietnamese-text")
                .attr("contenteditable", true)
                .addClass("active");

            vocabElement
                .find(".english-text,.vietnamese-text")
                .on("focus", function () {
                    $(this).addClass("focus");
                });

            vocabElement
                .find(".english-text,.vietnamese-text")
                .on("focusout", function () {
                    $(this).removeClass("focus");
                })
                .on("click", function (e) {
                    e.stopPropagation();
                });

            vocabElement.find(".english-text").focus();

            previousEditedVocabulary = {
                url: $btnEdit.data("url"),
                element: vocabElement,
            };
        } catch (error) {
            console.log("HandleEditVocabulary: ", error);
        }
    };

    const HandleDisableEdit = function () {
        try {
            // Khi click ra ngoài thì sẽ disable chế độ edit
            if (previousEditedVocabulary) {
                const englishTextElement =
                    previousEditedVocabulary.element.find(".english-text");
                const vietnameseTextElement =
                    previousEditedVocabulary.element.find(".vietnamese-text");

                englishTextElement
                    .attr("contenteditable", false)
                    .removeClass("active");

                vietnameseTextElement
                    .attr("contenteditable", false)
                    .removeClass("active");

                previousEditedVocabulary.element
                    .find(".btn-speech")
                    .data("text", englishTextElement.text());

                // Update lại thông tin từ vựng
                if (
                    englishTextElement.text().trim() !==
                        englishTextElement.data("old_value") ||
                    vietnameseTextElement.text().trim() !==
                        vietnameseTextElement.data("old_value")
                ) {
                    UpdateVocabularyItem();
                }
            }
        } catch (error) {
            console.log("HandleDisableEdit: ", error);
        }
    };

    /**
     * Tiến hành update lại thông tin từ vựng vào database
     *
     * Author: TaiPV, created at 13/05/2024
     */
    const UpdateVocabularyItem = function () {
        try {
            // Tiến hành update lại thông tin từ vựng
            const english = previousEditedVocabulary.element
                .find(".english-text")
                .text();

            const vietnamese = previousEditedVocabulary.element
                .find(".vietnamese-text")
                .text();

            const isStared = previousEditedVocabulary.element
                .find(".btn-star")
                .hasClass("active");

            const data = {
                sectionClassId,
                english: english.trim(),
                vietnamese: vietnamese.trim(),
                isStared,
            };

            $.ajax({
                url: previousEditedVocabulary.url,
                type: "POST",
                data: data,
                dataType: "json",
                success: function (response) {
                    if (response.code === 200) {
                        CommonModule.ShowToast("success", "Lưu thành công.");

                        // Cập nhật lại data trên UI
                        UpdateVocabularyDataOnUI(data.english, data.vietnamese);

                        previousEditedVocabulary = null;
                    } else {
                        CommonModule.ShowToast("error", response.message);
                    }
                },
                error: function (error) {
                    console.log(error);
                    CommonModule.ShowToast(
                        "error",
                        "Có lỗi xảy ra khi gửi yêu cầu."
                    );
                },
            });
        } catch (error) {
            CommonModule.ShowToast("error", "Có lỗi xảy ra phía Client");
        }
    };

    const HandleUpdateStar = function ($btnStar) {
        try {
            const indexOnOriginalData = $btnStar.data("index");
            $btnStar.toggleClass("active");

            originalVocabularies[indexOnOriginalData].is_stared =
                $btnStar.hasClass("active");
            previousEditedVocabulary = {
                url: $btnStar.data("url"),
                element: $btnStar.closest(".vocabulary-item"),
            };

            UpdateVocabularyItem();
        } catch (error) {}
    };

    /**
     * Vì chỉ cập nhật dữ liệu trên UI chứ không gọi API mỗi khi lựa chọn chế độ xem
     * nên khi gọi update từ vựng xong thì cập nhật lại dữ liệu trên UI luôn
     *
     * Author: TaiPV, created at 14/05/2024
     */
    const UpdateVocabularyDataOnUI = function (english, vietnamese) {
        try {
            previousEditedVocabulary.element
                .find(".english-text")
                .text(english)
                .data("old_value", english);

            previousEditedVocabulary.element
                .find(".vietnamese-text")
                .text(vietnamese)
                .data("old_value", vietnamese);

            previousEditedVocabulary.element
                .find(".btn-speech")
                .data("text", english);

            const updatedElementIndex = previousEditedVocabulary.element
                .find(".btn-star")
                .data("index");
            originalVocabularies[updatedElementIndex].english = english;
            originalVocabularies[updatedElementIndex].vietnamese = vietnamese;

            // Cập nhật lại dữ liệu của flashcard hiện tại
            if (currentVocabIndex == updatedElementIndex) {
                $(".front p").text(english);
                $(".back p").text(vietnamese);
                $("#card .btn-speech").data("text", english);
            }
        } catch (error) {
            console.log("UpdateVocabularyDataOnUI: ", error);
        }
    };

    let currentMembers = new Set();
    const LoadUsersToUI = function (template, users, type) {
        users.forEach((user) => {
            currentMembers.add(user.email);
            const newMemberRowTemplate = template.clone();
            newMemberRowTemplate.find(".avatar").attr("src", user.picture);
            newMemberRowTemplate.find(".display-name").text(user.display_name);
            newMemberRowTemplate.find(".email").text(user.email);
            newMemberRowTemplate.find(".member-role").text(type);
            $(".members-list").append(newMemberRowTemplate);
        });
    };

    const GetCurrentMembers = function () {
        try {
            $.ajax({
                type: "GET",
                dataType: "json",
                url: urls.getMembers,
                success: function (response) {
                    if (response.code === 200) {
                        $(".members-list").empty();

                        const members = response.data.members;
                        const pendingMembers = response.data.pending_members;
                        const memberRowTemplate = $(".member-row-template")
                            .clone()
                            .removeClass("dis-none member-row-template")
                            .addClass("d-flex");

                        LoadUsersToUI(memberRowTemplate, members, "Thành viên");
                        LoadUsersToUI(
                            memberRowTemplate,
                            pendingMembers,
                            "Đang chờ"
                        );
                    }
                },
                error: function (error) {
                    console.log(error);
                },
            });
        } catch (error) {
            console.log("GetCurrentMembers: ", error);
        }
    };

    const SearchUsers = function ($input) {
        // Sử dụng kĩ thuật debounce để tránh gửi request liên tục
        const query = $input.val();
        if (query.length < 3) {
            $(".suggestion-users").empty();
            $(".btn-submit-share").prop("disabled", true);
            return;
        }
        $(".btn-submit-share").prop("disabled", false);
        clearTimeout(debounceTimeout);

        debounceTimeout = setTimeout(function () {
            SearchUsersHandler(query);
        }, 200);
    };

    const SearchUsersHandler = function (query) {
        try {
            $.ajax({
                url: urls.searchUsers,
                type: "GET",
                data: { query },
                success: function (response) {
                    if (response.code === 200) {
                        const users = response.data;
                        $(".suggestion-users").empty();

                        const userElement = $(
                            ".suggestion-user-template.dis-none"
                        )
                            .clone()
                            .removeClass("dis-none");
                        users.forEach((user) => {
                            if (!currentMembers.has(user.email)) {
                                const newUserElement = userElement
                                    .clone()
                                    .addClass("new-user-element");

                                newUserElement
                                    .find(".avatar")
                                    .attr("src", user.picture);
                                newUserElement
                                    .find(".display-name")
                                    .text(user.display_name);
                                newUserElement.find(".email").text(user.email);
                                $(".suggestion-users").append(newUserElement);
                            }
                        });
                    }
                },
                error: function (error) {
                    console.log(error);
                },
                complete: function () {
                    CommonModule.SetLoading(false);
                },
            });
        } catch (error) {
            console.log("SearchUsersHandler: ", error);
        }
    };

    const HandleSharingToUser = function () {
        try {
            $.ajax({
                url: urls.shareToUser,
                dataType: "json",
                type: "POST",
                data: {
                    email: $("#search-email").val(),
                },
                success: function (response) {
                    console.log(response);
                    if (response.code === 200) {
                        $("#search-email").val("");
                        CommonModule.ShowToast("success", "Đã gửi yêu cầu.");

                        // Trigger lại sự kiện để load lại danh sách thành viên
                        GetCurrentMembers();
                    } else {
                        CommonModule.ShowToast("error", response.message);
                    }
                },
                error: function (error) {
                    console.log(error);
                    CommonModule.ShowToast(
                        "error",
                        "Có lỗi xảy ra khi gửi yêu cầu."
                    );
                },
            });
        } catch (error) {
            console.log("HandleSharingToUser: ", error);
        }
    };

    /**
     * Phản hồi lại lời mời tham gia lớp học
     *
     * Author: TaiPV, created at 14/05/2024
     * @param {JQueryElement} $btn: Accept or Decline button
     */
    const HandleResponseInvitation = function ($btn) {
        try {
            const status = $btn.data("status");
            $.ajax({
                url: urls.responseInvitation,
                data: { status: status },
                type: "POST",
                dataType: "json",
                success: function (response) {
                    console.log(response);
                    if (response.code === 200) {
                        if (status === "accept") {
                            CommonModule.ShowToast(
                                "success",
                                "Chúc mừng bạn đã tham gia lớp học thành công."
                            );

                            setTimeout(function () {
                                location.reload();
                            }, 1500);
                        } else {
                            CommonModule.ShowToast(
                                "info",
                                "Bạn đã từ chối lời mời. <br/> Sẽ chuyển bạn về trang chủ sau 2s."
                            );

                            setTimeout(function () {
                                window.location.href = "/";
                            }, 2000);
                        }
                    } else {
                        CommonModule.ShowToast("error", response.message);
                    }
                },
                error: function () {
                    CommonModule.ShowToast(
                        "error",
                        "Có lỗi xảy ra khi gửi yêu cầu."
                    );
                },
            });
        } catch (error) {}
    };

    /**
     * Redirect to do exam page
     *
     * Author: ManhTD, created at 23/05/2024
     */
        const CheckAndNavigateDoExam = function () {
            try {
                $.ajax({
                    url: urls.doExam,
                    type: "GET",
                    dataType: "json",
                    success: function (response) {
                        if (response.success) {
                            window.location.href = response.redirect_url;
                        } else {
                            CommonModule.ShowToast("error", response.error);
                        }
                    },
                    error: function (response) {
                        if (response.status == 400) {
                            CommonModule.ShowToast("error", response.responseJSON.error);
                        } else {
                            CommonModule.ShowToast(
                                "error",
                                "Có lỗi xảy ra khi gửi yêu cầu."
                            );
                        }
                    },
                });
            } catch (error) {}
        };

    return {
        Init: Init,
        InitEvents: InitEvents,
    };
})();
