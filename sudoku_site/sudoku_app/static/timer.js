// Set the time we're starting with
var start_of_time = new Date().getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // Get current time
  var now = new Date().getTime();

  // Find the distance between now and the start
  var distance = now - start_of_time;

  // Time calculations for days, hours, minutes and seconds
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
  //Adjust format
  var hours_first_digit = ""
  var minutes_first_digit = ""
  var seconds_first_digit = ""
  if (hours<10) {
    hours_first_digit = "0"
  }

  if (minutes<10) {
    minutes_first_digit = "0"
  }

  if (seconds<10){
    seconds_first_digit = "0"
  }

  // Display the result in the element with id "time-wrapper" (if present)
  timer_el = document.getElementById("timer-wrapper")
  if (timer_el != null){
    timer_el.innerHTML = hours_first_digit + hours + ":"
    + minutes_first_digit + minutes + ":" + seconds_first_digit + seconds ;
  }

}, 1000);