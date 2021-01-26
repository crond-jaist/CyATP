
let counter = 30;
let currentQuestion = 0;
let score = 0;
let lost = 0;
let record = [];
let timer;



//After the time has passed, have not selected any question, go to the next question
function nextQuestion() {
    const isQuestionOver = (quizQuestions.length - 1) === currentQuestion;
    if (isQuestionOver) {
        // TODO
        console.log('Game is over!!!!!');
        displayResult();
        // $('#feedback').hide();

    } else {
        currentQuestion++;
        loadQuestion();
        // $('#feedback').show();
    }
    
}

// 30 seconds to answer each question
function timeUp() {
    clearInterval(timer);

    lost++;
    record.push(2);

    preloadImage('lost');
    setTimeout(nextQuestion, 3 * 1000);
}

function countDown() {
    counter--;

    $('#time').html('Timer: ' + counter);

    if (counter === 0) {
        timeUp();
    }
}


// Random number
function getRandomArrayElements(arr, count) {
    var shuffled = arr.slice(0), i = arr.length, min = i - count, temp, index;
    while (i-- > min) {
        index = Math.floor((i + 1) * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    return shuffled.slice(min);
}


// Display the question and the choices to the browser
function loadQuestion() {
    counter = 30;
    timer = setInterval(countDown, 1000);
    $('#feedback').show();

    const question = quizQuestions[currentQuestion].question; //
    const choices = quizQuestions[currentQuestion].decided_choices; //


    $('#time').html('Timer: ' + counter);
    $('#game').html(`

        <h2 class="qst" id="qst">${question}</h2> 
        <button  class="btn btn-secondary btn-sm" onclick="copyToClipboard('#qst')" style="position: absolute; left: 650px">Copy</button>
        <br/>
            <script>
            function copyToClipboard(element) {
              var $temp = $("<input>");
              $("body").append($temp);
              $temp.val($(element).text()).select();
              document.execCommand("copy");
              $temp.remove();
            }
            </script>
        ${loadChoices(choices)}
        ${loadRemainingQuestion()}            

               
    `);
}

function loadChoices(choices) {
    let result = '';

    for (let i = 0; i < choices.length; i++) {
        result += `<p class="choice" data-answer="${choices[i]}" >${i+1}.  ${choices[i]}</p>`;
    }

    return result;
}

// Either correct/wrong choice selected, go to the next question
// Event Delegation
$(document).on('click', '.choice', function() {
    clearInterval(timer);
    const selectedAnswer = $(this).attr('data-answer');
    const correctAnswer = quizQuestions[currentQuestion].answer;


    console.log(quizQuestions[currentQuestion].answer)

    if (correctAnswer === selectedAnswer) {
        score++;
        record.push(1);
        console.log('Winsss!!!!');
        preloadImage('win');
        setTimeout(nextQuestion, 3 * 1000);
    } else {
        lost++;
        record.push(0);
        console.log('Lost!!!!');
        preloadImage('lost');
        setTimeout(nextQuestion, 3 * 1000);
    }
});


function displayResult() {

    const pointsResult = score * 10
    const result = `

        <h3 class="preload-image; text-center">You get <b>${score}</b> question(s) right</h3>
        <h3 class="preload-image; text-center">You missed <b>${lost}</b> question(s)</h3>
        <h3 class="preload-image; text-center">You have got <b>${pointsResult}</b> point(s)</h3>
        <h3 class="preload-image; text-center">Total questions ${quizQuestions.length} question(s) </h3>
        <br/>
        <div style="text-align: center">
        <button class="btn btn-primary ;" id="reset">Reset Game</button> 
        <button class="btn btn-primary ;" id="detail">Detail</button>                     
        <div>
`;
    $('#feedback').hide();
    $('#game').html(result);
}


$(document).on('click', '#reset', function() {
    counter = 30;
    currentQuestion = 0;
    score = 0;
    lost = 0;
    record = [];
    timer = null;

    loadQuestion();
});


$(document).on('click', '#detail', function() {
    StandardPost('feedback', quizQuestions, record);
    // window.location.href = 'feedback' ;
});



function loadRemainingQuestion() {
    const remainingQuestion = quizQuestions.length - (currentQuestion + 1);
    const totalQuestion = quizQuestions.length;
    const gotpoint = score *10;

    return `<br/><h4>Remaining Question(s): ${remainingQuestion}/${totalQuestion}</h4><br/><h4>Your Score: ${gotpoint}</h4>`;
}


function randomImage(images) {
    const random = Math.floor(Math.random() * images.length);
    const randomImage = images[random];
    return randomImage;
}


// Display  correct and wrong answers
function preloadImage(status) {
    const correctAnswer = quizQuestions[currentQuestion].answer;
    $('#feedback').hide();
    if (status === 'win') {
        $('#game').html(`

                <h3 class="text-center"><span style="color:red">Congratulations</span>, you pick the correct answer</h3>
                
                <h3 class="text-center">The correct answer is <b>${correctAnswer}</b></h3>
                
                <h3 class="text-center">You got <b>10</b> points.</h3>

        
        `);
    } else {
        $('#game').html(`
           
            
            <h3 class="text-center">The correct answer was <b>${correctAnswer}</b></h3>
            
            <h3 class="preload-image; text-center">You <span style="color:red">lost</span> pretty bad</h3>
            
            
        `);
    }
}


function StandardPost (url, args, arg2) {
    var myForm = document.createElement("form");
    myForm.method = "post";
    myForm.action = url;
    for (var k in args) {
        var myInput = document.createElement("input");
        myInput.setAttribute("name", k);
        myInput.setAttribute("value", [args[k]['question'], 'answer', args[k]['answer']]);
        myForm.appendChild(myInput);
    }

    var input2 = document.createElement("input");
    input2.setAttribute("name", 'record');
    input2.setAttribute("value", arg2);
    console.log(input2)

    myForm.appendChild(input2);
    document.body.appendChild(myForm);
    console.log(myForm);
    myForm.submit();
    document.body.removeChild(myForm);
}


function load_Q(){
        $.ajax({
                url: '/get_question',
                async: false,
                success: function(data) {
                    allQuestions = data;
                }
            });

    // 10 questions randomly selected
    quizQuestions = getRandomArrayElements(allQuestions, 10);
    console.log(quizQuestions);
}



$('#start').click(function() {
    $('#start').remove();
    $('#time').html(counter);
    load_Q();
    loadQuestion();
});