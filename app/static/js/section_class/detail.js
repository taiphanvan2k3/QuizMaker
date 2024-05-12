$(document).ready(function () {
    SectionClassDetailModule.InitEvents();
});

const SectionClassDetailModule = (function () {
    let currentVocabIndex = 0;
    let originalVocabularies = vocabData;
    let currentVocabularies = [...originalVocabularies];
    let vocabCount = vocabData.length;
    let learnedVocabularies = [];
    let learningVocabularies = [];
    const btnChecked = $(".btn-checked");

    // Lưu trạng thái hành động trước đó
    let previousAction;

    const InitEvents = function () {
        $("#card").on("click", function () {
            $(this).toggleClass("turned");
        });

        $(".btn-x, .btn-checked").on("click", function () {
            HandleNextVocab($(this));
        });

        $(".btn-speech").on("click", function (e) {
            GetAudioFromText($(this).data("text"));
            e.stopPropagation();
        });

        $(".btn-revert").prop("disabled", true);
        $(".btn-revert").on("click", HandleRevertVocab);

        $(".review-block").on("click", SetDataForReviewing);
        $(".learn-again-block").on("click", ResetData);
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
                $(".btn-speech").data("text", vocab.english);
                if ($("#is-auto-audio").is(":checked")) {
                    GetAudioFromText(vocab.english);
                }
            }
            currentVocabIndex++;

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

            $(".learning-message").addClass("active");
            setTimeout(function () {
                $(".learning-message").removeClass("active");
            }, 300);

            currentVocabIndex--;
            const vocab = currentVocabularies[currentVocabIndex];
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
    const GetAudioFromText = function (text) {
        try {
            $(".btn-speech").addClass("active");
            const audio = new SpeechSynthesisUtterance(text);
            audio.lang = "en-US";
            audio.voice = window.speechSynthesis.getVoices()[5];
            window.speechSynthesis.speak(audio);
            audio.onend = function () {
                $(".btn-speech").removeClass("active");
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
    };

    return {
        InitEvents: InitEvents,
    };
})();
