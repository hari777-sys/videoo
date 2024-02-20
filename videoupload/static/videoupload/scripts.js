window.addEventListener("scroll", function(){
    var header = document.querySelector("header");
    header.classList.toggle('sticky', window.scrollY > 0);
});

var menu = document.querySelector('.menu');
var menuBtn = document.querySelector('.menu-btn');
var closeBtn = document.querySelector('.close-btn');

menuBtn.addEventListener("click",() => {
    menu.classList.add('active');
});

closeBtn.addEventListener("click",() => {
    menu.classList.remove('active');
});
document.getElementById('id_video_file').addEventListener('change', function() {
    var fileName = this.files[0].name;
    if (!fileName.toLowerCase().endsWith('.mp4')) {
        alert('Only .mp4 files are allowed.');
        // Clear the file input to prevent submission
        this.value = '';
    }
});

const optionButtons = document.querySelectorAll('.options-btn');
    const optionMenus = document.querySelectorAll('.options-menu');

    // Iterate over each button and add click event listener
    optionButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            // Toggle visibility of the menu
            optionMenus[index].classList.toggle('show');
        });
    });



