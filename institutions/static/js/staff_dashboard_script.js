
		i = -1;
		function StudentCounting() {
			i++;
			return studentCounting[i];
		};
		
		var config = {	
			type: 'pie',
			data: {
				datasets: [{
					data: [
						StudentCounting(),
						StudentCounting(),
					],
					backgroundColor: [
						window.chartColors.red,
						window.chartColors.blue,
					],
					label: 'Dataset 1',
					
				}],
				labels: [
					'Male Students',
					'Female Students',
				]
			},
			showDatapoints: true,
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Total Male/Female Students'
				},
				pieceLabel: {
				    render: 'percentage',
				    fontColor: 'black',
				    precision: 2,
				    fontSize: 25,
				    fontStyle: 'italic'
				},
				
			}
		};
		window.onload = function() {
			var ctx = document.getElementById('chart-area').getContext('2d');
			window.myPie = new Chart(ctx, config);
		};
