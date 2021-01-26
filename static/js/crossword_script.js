
$old_jquery(function($) {
	$(function() {
		$old_jquery.ajax({
			url: '/get_cross',
			async: false,
			success: function(data) {
				puzzleData = data

				// console.log(puzzleData)
				// console.log(quizQuestions[1].answer)

				// const question = quizQuestions[currentQuestion].question; //
				// const choices = quizQuestions[currentQuestion].other_choice; //

			}
		});
      	// console.log(puzzleData);

		$('#puzzle-wrapper').crossword(puzzleData);
	})

});
//(jQuery)
