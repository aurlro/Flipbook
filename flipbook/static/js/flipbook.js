/**
 * Flipbook JavaScript Module
 * Version: 1.0.1
 * Author: aurlro
 * Last Updated: 2024-02-24 13:47:38
 */

class FlipbookErrorBoundary {
    constructor(container) {
        this.container = container;
    }

    handleError(error) {
        console.error('Flipbook error:', error);
        this.container.innerHTML = `
            <div class="error-message">
                <p>Une erreur est survenue lors du chargement du flipbook.</p>
                <button onclick="location.reload()">Réessayer</button>
            </div>
        `;
    }
}

class Flipbook {
    constructor(options = {}) {
        // Configuration par défaut
        this.config = {
            container: options.container || '.flipbook-container',
            pageWidth: options.pageWidth || 800,
            pageHeight: options.pageHeight || 600,
            duration: options.duration || 800,
            perspective: options.perspective || 2500,
            zoomEnabled: options.zoomEnabled || true,
            maxZoom: options.maxZoom || 2,
            minZoom: options.minZoom || 0.5,
            preloadCount: options.preloadCount || 3
        };

        // État interne
        this.state = {
            pages: [],
            currentPage: 0,
            isAnimating: false,
            zoom: 1,
            isDragging: false,
            startX: 0,
            currentX: 0,
            touchStartX: 0
        };

        // Initialisation de l'ErrorBoundary
        this.errorBoundary = null;

        this.init();
    }

    /**
     * Initialisation du flipbook
     */
    init() {
        try {
            this.container = document.querySelector(this.config.container);
            if (!this.container) {
                throw new Error('Container not found');
            }

            this.errorBoundary = new FlipbookErrorBoundary(this.container);
            this.setupContainer();
            this.bindEvents();
            this.setupUploadHandler();

        } catch (error) {
            if (this.errorBoundary) {
                this.errorBoundary.handleError(error);
            } else {
                console.error('Failed to initialize Flipbook:', error);
            }
        }
    }

    /**
     * Préchargement des images
     * @param {Array<string>} sources - Liste des URLs des images
     * @returns {Promise<Array<HTMLImageElement>>}
     */
    async preloadImages(sources) {
        try {
            return await Promise.all(sources.map(src => {
                return new Promise((resolve, reject) => {
                    const img = new Image();
                    img.onload = () => resolve(img);
                    img.onerror = () => reject(`Failed to load image: ${src}`);
                    img.src = src;
                });
            }));
        } catch (error) {
            this.errorBoundary.handleError(error);
            throw error;
        }
    }

    /**
     * Chargement paresseux des images
     * @param {number} startIndex - Index de départ
     * @param {number} count - Nombre d'images à charger
     */
    lazyLoadImages(startIndex, count = this.config.preloadCount) {
        try {
            const endIndex = Math.min(startIndex + count, this.state.pages.length);
            for (let i = startIndex; i < endIndex; i++) {
                if (!this.state.pages[i].loaded) {
                    const img = new Image();
                    img.src = this.state.pages[i].src;
                    img.dataset.pageIndex = i;
                    img.onload = () => {
                        this.state.pages[i].loaded = true;
                    };
                }
            }
        } catch (error) {
            this.errorBoundary.handleError(error);
        }
    }

    /**
     * Création d'une page
     * @param {number} pageNumber - Numéro de la page
     * @param {boolean} isBack - Si c'est le verso de la page
     * @returns {HTMLElement}
     */
    createPage(pageNumber, isBack = false) {
        try {
            const page = document.createElement('div');
            page.className = `page ${isBack ? 'back' : ''}`;

            const frontDiv = document.createElement('div');
            frontDiv.className = 'page-front';
            const backDiv = document.createElement('div');
            backDiv.className = 'page-back';

            const img = document.createElement('img');
            img.className = 'page-img';
            img.src = this.state.pages[pageNumber].src;
            img.alt = `Page ${pageNumber + 1}`;

            if (isBack) {
                backDiv.appendChild(img.cloneNode());
                page.append(backDiv, frontDiv);
            } else {
                frontDiv.appendChild(img);
                page.append(frontDiv, backDiv);
            }

            return page;
        } catch (error) {
            this.errorBoundary.handleError(error);
            throw error;
        }
    }

    /**
     * Gestion de la navigation
     * @param {'next'|'prev'} direction - Direction de la navigation
     */
    handleNavigation(direction) {
        try {
            if (this.state.isAnimating) return;

            if (direction === 'next') {
                this.flipPage();
            } else if (direction === 'prev') {
                this.flipPageBack();
            }
        } catch (error) {
            this.errorBoundary.handleError(error);
        }
    }

    /**
     * Animation de page vers l'avant
     */
    flipPage() {
        try {
            if (this.state.currentPage >= this.state.pages.length - 1 ||
                this.state.isAnimating) {
                return;
            }

            this.state.isAnimating = true;
            const newPage = this.createPage(this.state.currentPage + 1, true);
            this.container.appendChild(newPage);

            requestAnimationFrame(() => {
                newPage.style.transform = 'rotateY(-180deg)';
                this.state.currentPage++;
                this.lazyLoadImages(this.state.currentPage + 1);

                setTimeout(() => {
                    this.state.isAnimating = false;
                }, this.config.duration);
            });
        } catch (error) {
            this.state.isAnimating = false;
            this.errorBoundary.handleError(error);
        }
    }

    /**
     * Animation de page vers l'arrière
     */
    flipPageBack() {
        try {
            if (this.state.currentPage <= 0 || this.state.isAnimating) {
                return;
            }

            this.state.isAnimating = true;
            const pages = this.container.querySelectorAll('.page');
            const lastPage = pages[pages.length - 1];

            lastPage.style.transform = 'rotateY(0deg)';
            setTimeout(() => {
                this.container.removeChild(lastPage);
                this.state.currentPage--;
                this.state.isAnimating = false;
            }, this.config.duration);
        } catch (error) {
            this.state.isAnimating = false;
            this.errorBoundary.handleError(error);
        }
    }

    // ... [Autres méthodes de la classe Flipbook restent inchangées]

    /**
     * Gestion des événements utilisateur
     * @param {Event} e - Événement
     */
    handleUserInput(e) {
        try {
            switch(true) {
                case e.type === 'click':
                    this.handleNavigation('next');
                    break;

                case e.type === 'keydown' && e.key === 'ArrowRight':
                    this.handleNavigation('next');
                    break;

                case e.type === 'keydown' && e.key === 'ArrowLeft':
                    this.handleNavigation('prev');
                    break;

                case e.type === 'touchstart':
                    this.state.touchStartX = e.changedTouches[0].screenX;
                    break;

                case e.type === 'touchend':
                    const deltaX = e.changedTouches[0].screenX -
                                 this.state.touchStartX;
                    if (Math.abs(deltaX) > 50) {
                        this.handleNavigation(deltaX > 0 ? 'prev' : 'next');
                    }
                    break;
            }
        } catch (error) {
            this.errorBoundary.handleError(error);
        }
    }
}

// Initialisation sécurisée du flipbook
document.addEventListener('DOMContentLoaded', () => {
    try {
        window.flipbook = new Flipbook({
            container: '.flipbook-container',
            pageWidth: 800,
            pageHeight: 600,
            duration: 800,
            zoomEnabled: true,
            preloadCount: 3
        });

        // Charger les images initiales si elles existent déjà
        const initialPages = [
            'images/page1.jpg',
            'images/page2.jpg',
            'images/page3.jpg'
        ];

        if (window.flipbook && initialPages.length > 0) {
            window.flipbook.preloadImages(initialPages)
                .then(images => {
                    images.forEach((img, index) => {
                        window.flipbook.state.pages.push({
                            src: initialPages[index],
                            loaded: true
                        });
                    });
                    window.flipbook.container.appendChild(
                        window.flipbook.createPage(0)
                    );
                })
                .catch(error => {
                    if (window.flipbook.errorBoundary) {
                        window.flipbook.errorBoundary.handleError(error);
                    }
                });
        }
    } catch (error) {
        console.error('Failed to initialize Flipbook:', error);
        const container = document.querySelector('.flipbook-container');
        if (container) {
            const errorBoundary = new FlipbookErrorBoundary(container);
            errorBoundary.handleError(error);
        }
    }
});
