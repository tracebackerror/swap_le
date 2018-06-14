		
		i = -1;
		function TotalQuestionsFunction() {
			i++;
			return total_questions[i];
		};
		
		j = -1;
		function AttemptedQuestionFunction() {
			j++;
			return attempted_questions[j];
		};
		
		k = -1;
		function CorrectedQuestionsFunction() {
			k++;
			return corrected_questions[k];
		};
		
		
		var CallTotalQuestions = [];
		var CallAttemptedQuestions = [];
		var CallCorrectedQuestions = [];
		for(a=0;a<section.length;a++)
		{
			CallTotalQuestions.push(TotalQuestionsFunction());
			CallAttemptedQuestions.push(AttemptedQuestionFunction());
			CallCorrectedQuestions.push(CorrectedQuestionsFunction());
		};
		
		
		
		var config = {
			type: 'line',
			data: {
				labels: section,
				datasets: [{
					label: 'Total Question',
					fill: false,
					backgroundColor: window.chartColors.red,
					borderColor: window.chartColors.red,
					data: CallTotalQuestions,
					
				},{
					label: 'Attempted Questions',
					fill: false,
					backgroundColor: window.chartColors.blue,
					borderColor: window.chartColors.blue,
					data: CallAttemptedQuestions,
					
				}, {
					label: 'Corrected Questions',
					fill: false,
					backgroundColor: window.chartColors.green,
					borderColor: window.chartColors.green,
					data: CallCorrectedQuestions,
				}]
			},
			
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Section Wise Student Result Graph View'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'SECTION NAME'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'QUESTIONS'
						},
						ticks: {
							min: 0,
							max: 20,

							// forces step size to be 5 units
							stepSize: 1
						}
					}]
				}
			}
		};

		window.onload = function() {
			var ctx = document.getElementById('canvas').getContext('2d');
			window.myLine = new Chart(ctx, config);
		};



