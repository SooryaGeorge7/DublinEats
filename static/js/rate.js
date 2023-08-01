

var form = document.querySelector('.reviewform');

var handleRatings = (choice, criteria) => {
  var stars = document.querySelectorAll(`.${criteria} .btn i`);

  stars.forEach(star => star.classList.remove('checked'));

  switch (choice) {
    case 'first':
      for (var i = 0; i < 1; i++) {
        stars[i].classList.add('checked');
      }
      break;
    case 'second':
      for (var i = 0; i < 2; i++) {
        stars[i].classList.add('checked');
      }
      break;
    case 'third':
      for (var i = 0; i < 3; i++) {
        stars[i].classList.add('checked');
      }
      break;
    case 'fourth':
      for (var i = 0; i < 4; i++) {
        stars[i].classList.add('checked');
      }
      break;
    case 'fifth':
      for (var i = 0; i < 5; i++) {
        stars[i].classList.add('checked');
      }
      break;
  }

  var val_num = getNumValue(choice);
  form[criteria].value = val_num;
};

var getNumValue = (stringValue) => {
  let numValue;
  if (stringValue === 'first') {
    numValue = 1;
  } else if (stringValue === 'second') {
    numValue = 2;
  } else if (stringValue === 'third') {
    numValue = 3;
  } else if (stringValue === 'fourth') {
    numValue = 4;
  } else if (stringValue === 'fifth') {
    numValue = 5;
  } else {
    numValue = 0;
  }
  return numValue;
};

var criterias = ['taste', 'ambience', 'customer_service', 'location', 'value_for_money'];

criterias.forEach(criteria => {
  var stars = document.querySelectorAll(`.${criteria} .btn i`);

  stars.forEach(star => {
    star.addEventListener('click', (event) => {
      handleRatings(event.target.id, criteria);
    });
  });
});

// Function to set the star ratings based on the user's previous review
var updateStarRatings = (criteria) => {
  var stars = document.querySelectorAll(`.${criteria} .btn i`);
  var value = form[criteria].value;

  stars.forEach((star, index) => {
    if (index < value) {
      star.classList.add('checked');
    } else {
      star.classList.remove('checked');
    }
  });
};

// Call updateStarRatings for each criteria to set the initial star ratings based on the user's previous review
criterias.forEach(criteria => {
  updateStarRatings(criteria);
});



