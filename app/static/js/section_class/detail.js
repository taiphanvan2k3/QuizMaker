$(document).ready(function () {
    SectionClassDetailModule.InitEvents();
});

const SectionClassDetailModule = (function () {
    let currentVocabIndex = 0;
    const vocabCount = vocabularies.length;
    const learnedVocabularies = [];
    const learningVocabularies = [];
    const btnChecked = $(".btn-checked");

    const InitEvents = function () {
        $("#card").on("click", function () {
            $(this).toggleClass("turned");
        });

        $(".fa-volume-high").on("click", function (e) {
            e.stopPropagation();
        });

        $(".btn-x, .btn-checked").on("click", function () {
            HandleNextVocab($(this));
        });
    };

    const HandleNextVocab = function ($btn) {
        try {
            if ($btn.prop("disabled") || currentVocabIndex == vocabCount) {
                return;
            }

            if ($btn[0] == btnChecked[0]) {
                learnedVocabularies.push(currentVocabIndex);
            } else {
                learningVocabularies.push(currentVocabIndex);
            }

            if (currentVocabIndex + 1 < vocabCount) {
                const vocab = vocabularies[currentVocabIndex + 1];
                $(".front p").text(vocab.english);
                $(".back p").text(vocab.vietnamese);
            }
            currentVocabIndex++;

            $(".counter").text(`${currentVocabIndex + 1} / ${vocabCount}`);
            if (currentVocabIndex === vocabCount - 1) {
                $btn.prop("disabled", true);
            }

            let message = ".learned-message";
            if ($btn[0] == btnChecked[0]) {
                $(".learned-message").addClass("active");
            } else {
                $(".learning-message").addClass("active");
                message = ".learning-message";
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
            }
        } catch (error) {
            console.log("HandleNextVocab: ", error);
        }
    };

    return {
        InitEvents: InitEvents,
    };
})();
