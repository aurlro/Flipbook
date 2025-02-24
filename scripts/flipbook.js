const pages = [
    'images/page1.jpg',
    'images/page2.jpg',
    'images/page3.jpg'
];

const container = document.querySelector('.flipbook-container');
let currentPage = 0;
let isAnimating = false;

// Préchargement des images
function preloadImages() {
    pages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

function createPage(pageNumber, isBack = false) {
    const page = document.createElement('div');
    page.className = `page ${isBack ? 'back' : ''}`;
    
    const frontDiv = document.createElement('div');
    frontDiv.className = 'page-front';
    const backDiv = document.createElement('div');
    backDiv.className = 'page-back';

    const img = document.createElement('img');
    img.className = 'page-img';
    img.src = pages[pageNumber];
    img.alt = `Page ${pageNumber + 1}`;

    if(isBack) {
        backDiv.appendChild(img.cloneNode());
        page.append(backDiv, frontDiv);
    } else {
        frontDiv.appendChild(img);
        page.append(frontDiv, backDiv);
    }

    return page;
}

function handleNavigation(direction) {
    if(isAnimating) return;
    
    if(direction === 'next') {
        flipPage();
    } else if(direction === 'prev') {
        flipPageBack();
    }
}

function flipPage() {
    if(currentPage < pages.length - 1 && !isAnimating) {
        isAnimating = true;
        const newPage = createPage(currentPage + 1, true);
        container.appendChild(newPage);
        
        requestAnimationFrame(() => {
            newPage.style.transform = 'rotateY(-180deg)';
            currentPage++;
            isAnimating = false;
        });
    }
}

function flipPageBack() {
    if(currentPage > 0 && !isAnimating) {
        isAnimating = true;
        const pages = container.querySelectorAll('.page');
        const lastPage = pages[pages.length - 1];
        
        lastPage.style.transform = 'rotateY(0deg)';
        setTimeout(() => {
            container.removeChild(lastPage);
            currentPage--;
            isAnimating = false;
        }, 800);
    }
}

// Gestion des événements
function handleUserInput(e) {
    switch(true) {
        case e.type === 'click':
            handleNavigation('next');
            break;
            
        case e.key === 'ArrowRight':
            handleNavigation('next');
            break;
            
        case e.key === 'ArrowLeft':
            handleNavigation('prev');
            break;
            
        case e.type === 'touchstart':
            const touchStartX = e.changedTouches[0].screenX;
            handleSwipe(touchStartX);
            break;
    }
}

// Gestion du swipe tactile
let touchStartX = 0;

function handleSwipe(startX) {
    const deltaX = startX - touchStartX;
    if(Math.abs(deltaX) > 50) {
        handleNavigation(deltaX > 0 ? 'prev' : 'next');
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    preloadImages();
    container.appendChild(createPage(0));
    
    // Événements
    document.addEventListener('click', handleUserInput);
    document.addEventListener('keydown', handleUserInput);
    document.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    });
    document.addEventListener('touchend', handleUserInput);
});
