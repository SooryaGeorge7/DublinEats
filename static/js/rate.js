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
            var val = event.target.id;
            var val_num = getNumValue(val);
            form[criteria].value = val_num;
        });
    });
});






// // get all the stars
// var one = document.getElementById('first');
// var two = document.getElementById('second');
// var three = document.getElementById('third');
// var four = document.getElementById('fourth');
// var five = document.getElementById('fifth');

// var form = document.querySelector('.reviewform');

// // get the hover stars and add/remove checked class
// var handleSelect = (selection) => {
//     switch (selection) {
//         case 'first': {
//             one.classList.add('checked');
//             two.classList.remove('checked');
//             three.classList.remove('checked');
//             four.classList.remove('checked');
//             five.classList.remove('checked');
//             return;

//         }
//         case 'second': {
//             one.classList.add('checked');
//             two.classList.add('checked');
//             three.classList.remove('checked');
//             four.classList.remove('checked');
//             five.classList.remove('checked');
//             return;

//         }
//         case 'third': {
//             one.classList.add('checked');
//             two.classList.add('checked');
//             three.classList.add('checked');
//             four.classList.remove('checked');
//             five.classList.remove('checked');
//             return;

//         }
//         case 'fourth': {
//             one.classList.add('checked');
//             two.classList.add('checked');
//             three.classList.add('checked');
//             four.classList.add('checked');
//             five.classList.remove('checked');
//             return;

//         }
//         case 'fifth': {
//             one.classList.add('checked');
//             two.classList.add('checked');
//             three.classList.add('checked');
//             four.classList.add('checked');
//             five.classList.add('checked');
//             return;

//         }
//     }
// };

// ///Get string value from stars and add numeric value 
// var getNumericValue = (stringValue) => {
//     let numericValue;
//     if (stringValue === 'first') {
//         numericValue = 1;
//     } else if (stringValue === 'second') {
//         numericValue = 2;
//     } else if (stringValue === 'third') {
//         numericValue = 3;
//     } else if (stringValue === 'fourth') {
//         numericValue = 4;
//     } else if (stringValue === 'fifth') {
//         numericValue = 5;
//     } else {
//         numericValue = 0;
//     }
//     return numericValue;
// };

// var arr = [one, two, three, four, five];

// ///Add event listener to mouse hover on rating stars
// // arr.forEach(item => item.addEventListener('mouseover', (event) => {
// //     handleSelect(event.target.id)

// // }))

// arr.forEach(item => item.addEventListener('click', (event) => {
//     handleSelect(event.target.id);

// }));

// /// Tranform string value from stars into numeric value 
// arr.forEach(item => item.addEventListener('click', (event) => {
//     var val = event.target.id;
//     var val_num = getNumericValue(val);
//     form.taste.value = val_num;
    
// }));


