		
		i = -1;
		function TotalQuestionsFunction() {
			i++;
			return total_questions[i];
		};
		
		
		
		var CallTotalQuestions = [];
		var CallAttemptedQuestions = [];
		var CallCorrectedQuestions = [];
		for(a=0;a<section.length;a++)
		{
			CallTotalQuestions.push(TotalQuestionsFunction());
			
		};
		
		
		
		var config = {
			type: 'line',
			data: {
				labels: section,
				datasets: [
					{
						label: 'Marks Obtained',
						fill: false,
						backgroundColor: window.chartColors.red,
						borderColor: window.chartColors.red,
						data: CallTotalQuestions,
						
					},
				]
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
							labelString: 'Marks'
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



