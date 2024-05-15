$(document).ready(function () {
    ExamSectionClassModule.Init();
    ExamSectionClassModule.InitEvents();
});

const ExamSectionClassModule = (function () {
    const Init = function () {
        
    };

    const InitEvents = function () {
        $('.answer-btn').on('click', function () {
            if($(this).hasClass('active')) {
                $(this).removeClass('active');
            } else {
                $(this).closest('.wrapper').find('.answer-btn').removeClass('active');
                $(this).toggleClass('active');
                scrollToNextQuestion.call(this);
            }
            updateProgressBar();
        });

        $('.btn-submit').click(function() {
            var chooseAns = [];
            var correctCount = 0;

            $('.wrapper').each(function(index) {
                var selectedBtn = $(this).find('.answer-btn.active');
                if (selectedBtn.length) {
                    chooseAns.push(selectedBtn.attr('index-ans'));
                } else {
                    chooseAns.push(-1);
                }
            });
    
            // So sánh và áp dụng các class tương ứng
            chooseAns.forEach((chosenIndex, i) => {
                var correctIndex = ansTrueArray[i].toString();
                var $currentWrapper = $('.wrapper').eq(i);
                var $selectedBtn = $currentWrapper.find(`.answer-btn[index-ans="${chosenIndex}"]`);
                var $correctBtn = $currentWrapper.find(`.answer-btn[index-ans="${correctIndex}"]`);
    
                if (chosenIndex !== correctIndex) {
                    if ($selectedBtn.length) {
                        $selectedBtn.addClass('incorrect-answer');
                    }
                    $correctBtn.addClass('correct-answer');
                    
                } else {
                    correctCount++;
                    $correctBtn.addClass('correct-answer');
                }
                $selectedBtn.removeClass('active');
            });
    
            // Tắt sự kiện click trên các nút answer-btn
            $('.answer-btn').off('click mouseenter mouseleave');
            // Hiển thị Radial Progress Bar và cập nhật giá trị
            var totalQuestions = chooseAns.length;
            var correctPercentage = (correctCount / totalQuestions) * 100;

            $('.text-complete').hide();
            $('.radial-progress').show().css('display', 'grid');  // Đảm bảo RadialProgress hiển thị
            setProgress(correctPercentage);
        });
    };

    function setProgress(progress) {
        const radialProgress = document.querySelector('.radial-progress');
        const value = `${progress.toFixed(0)}%`;
        radialProgress.style.setProperty('--progress', value);
        radialProgress.innerHTML = value;
        radialProgress.setAttribute('aria-valuenow', value);
    }

    function scrollToNextQuestion() {
        var $nextQuestion = $(this).closest('.wrapper').next('.wrapper');
        var offsetTopAdjustment = 100;
    
        requestAnimationFrame(function() {
            if ($nextQuestion.length) {
                $('html, body').animate({
                    scrollTop: $nextQuestion.offset().top - offsetTopAdjustment
                }, 700);
            } else {
                $('html, body').animate({
                    scrollTop: $('.footer').offset().top
                }, 700);
            }
        });
    }

    /**
     * Update progress bar
     * Author: ManhTD, created at 2024/05/14
     */
    function updateProgressBar() {
        var totalQuestions = lenQuiz;
        var answeredQuestions = $('.answer-btn.active').length;
        var progressPercentage = (answeredQuestions / totalQuestions) * 100;

        $('.progress-bar').css('--progress', progressPercentage + '%');
        $('.progress-bar').attr('style', '--progress: ' + progressPercentage + '%');
    }

    return {
        Init: Init,
        InitEvents: InitEvents,
    };
})();
