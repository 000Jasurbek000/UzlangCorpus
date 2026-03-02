// Kitob flipbook functionality
// Set PDF.js worker
if (typeof pdfjsLib !== 'undefined') {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
}

// Initialize flipbook when DOM is ready
function initFlipbook(bookData) {
    const totalPages = parseInt(bookData.pages);
    const bookTitle = bookData.title;
    const bookAuthor = bookData.author;
    const bookPublisher = bookData.publisher;
    const bookYear = bookData.year;
    const bookISBN = bookData.isbn;
    const pdfUrl = bookData.pdf_url;
    
    // Create flipbook
    const pageFlip = new St.PageFlip(document.getElementById('flipbook'), {
        width: 550,  // Half of book width
        height: 733, // Page height
        size: 'fixed',
        minWidth: 315,
        maxWidth: 1000,
        minHeight: 420,
        maxHeight: 1350,
        maxShadowOpacity: 0.5,
        showCover: true,
        mobileScrollSupport: true,
        swipeDistance: 30,
        clickEventForward: true,
        usePortrait: true,
        startPage: 0,
        drawShadow: true,
        flippingTime: 1000,
        useMouseEvents: true,
        autoSize: true,
        showPageCorners: true,
        disableFlipByClick: false
    });
    
    // Load and render PDF
    let pdfDoc = null;
    
    // Load PDF document
    console.log('Loading PDF from:', pdfUrl);
    pdfjsLib.getDocument(pdfUrl).promise.then(function(pdf) {
        pdfDoc = pdf;
        console.log('PDF loaded successfully, pages:', pdf.numPages);
        
        // Generate pages
        const pages = [];
        
        // Cover page
        pages.push(createCoverPage(bookTitle, bookAuthor, bookPublisher, bookYear));
        
        // Generate PDF page canvases
        generatePDFPages(pdf, totalPages).then(function(pdfPages) {
            console.log('Generated', pdfPages.length, 'PDF pages');
            pdfPages.forEach(page => pages.push(page));
            
            // Back cover
            pages.push(createBackCoverPage(bookISBN));
            
            // Load pages into flipbook
            pageFlip.loadFromHTML(pages);
            console.log('Flipbook loaded with', pages.length, 'total pages');
        });
    }).catch(function(error) {
        console.error('Error loading PDF:', error);
        console.error('PDF URL was:', pdfUrl);
        alert('PDF yuklanmadi. Xatolik: ' + error.message + '\n\nDemo sahifalar ko\'rsatiladi.');
        // Fallback to demo pages if PDF fails
        loadDemoPages(pageFlip, totalPages, bookTitle, bookAuthor, bookPublisher, bookYear, bookISBN);
    });
    
    // Update page counter
    pageFlip.on('flip', (e) => {
        const currentPage = e.data;
        document.getElementById('currentPage').textContent = currentPage + 1;
        updateButtons(currentPage, totalPages);
    });
    
    // Button controls
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    prevBtn.addEventListener('click', () => {
        pageFlip.flipPrev();
    });
    
    nextBtn.addEventListener('click', () => {
        pageFlip.flipNext();
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            pageFlip.flipPrev();
        } else if (e.key === 'ArrowRight') {
            pageFlip.flipNext();
        }
    });
    
    // Initialize
    updateButtons(0, totalPages);
    document.getElementById('totalPages').textContent = totalPages + 2; // Include covers
}

async function generatePDFPages(pdf, totalPages) {
    const pdfPages = [];
    const numPages = Math.min(pdf.numPages, totalPages);
    
    for (let pageNum = 1; pageNum <= numPages; pageNum++) {
        const page = await pdf.getPage(pageNum);
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        
        const viewport = page.getViewport({ scale: 1.5 });
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        
        await page.render({
            canvasContext: context,
            viewport: viewport
        }).promise;
        
        // Create DOM element instead of HTML string
        const pageDiv = document.createElement('div');
        pageDiv.className = 'page';
        
        const pageContent = document.createElement('div');
        pageContent.className = 'page-content';
        
        const img = document.createElement('img');
        img.src = canvas.toDataURL();
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'contain';
        
        const pageNumber = document.createElement('div');
        pageNumber.className = 'page-number';
        pageNumber.style.position = 'absolute';
        pageNumber.style.bottom = '20px';
        pageNumber.style.left = '0';
        pageNumber.style.right = '0';
        pageNumber.style.textAlign = 'center';
        pageNumber.style.fontSize = '14px';
        pageNumber.style.color = '#666';
        pageNumber.textContent = pageNum;
        
        pageContent.appendChild(img);
        pageContent.appendChild(pageNumber);
        pageDiv.appendChild(pageContent);
        
        pdfPages.push(pageDiv);
    }
    
    return pdfPages;
}

function loadDemoPages(pageFlip, totalPages, bookTitle, bookAuthor, bookPublisher, bookYear, bookISBN) {
    const pages = [];
    
    // Cover page
    pages.push(createCoverPage(bookTitle, bookAuthor, bookPublisher, bookYear));
    
    // Content pages (demo)
    for (let i = 1; i <= totalPages; i++) {
        pages.push(createContentPage(i));
    }
    
    // Back cover
    pages.push(createBackCoverPage(bookISBN));
    
    // Load pages
    pageFlip.loadFromHTML(pages);
}

function createCoverPage(bookTitle, bookAuthor, bookPublisher, bookYear) {
    const pageDiv = document.createElement('div');
    pageDiv.className = 'page page--cover';
    pageDiv.setAttribute('data-density', 'hard');
    
    const pageContent = document.createElement('div');
    pageContent.className = 'page-content';
    pageContent.style.background = 'linear-gradient(135deg, var(--navy) 0%, var(--turquoise) 100%)';
    pageContent.style.color = 'white';
    pageContent.style.padding = '60px';
    pageContent.style.position = 'relative';
    
    const title = document.createElement('h1');
    title.style.fontSize = '36px';
    title.style.marginBottom = '20px';
    title.style.fontFamily = 'var(--font-serif)';
    title.style.textAlign = 'center';
    title.textContent = bookTitle;
    
    const author = document.createElement('p');
    author.style.fontSize = '20px';
    author.style.textAlign = 'center';
    author.style.marginTop = '40px';
    author.textContent = bookAuthor;
    
    const bottomDiv = document.createElement('div');
    bottomDiv.style.position = 'absolute';
    bottomDiv.style.bottom = '40px';
    bottomDiv.style.left = '0';
    bottomDiv.style.right = '0';
    bottomDiv.style.textAlign = 'center';
    
    const publisher = document.createElement('p');
    publisher.style.fontSize = '16px';
    publisher.style.opacity = '0.9';
    publisher.textContent = bookPublisher;
    
    const year = document.createElement('p');
    year.style.fontSize = '16px';
    year.style.opacity = '0.9';
    year.textContent = bookYear;
    
    bottomDiv.appendChild(publisher);
    bottomDiv.appendChild(year);
    
    pageContent.appendChild(title);
    pageContent.appendChild(author);
    pageContent.appendChild(bottomDiv);
    pageDiv.appendChild(pageContent);
    
    return pageDiv;
}

function createContentPage(pageNum) {
    const pageDiv = document.createElement('div');
    pageDiv.className = 'page';
    
    const pageContent = document.createElement('div');
    pageContent.className = 'page-content';
    
    const wrapper = document.createElement('div');
    wrapper.style.padding = '50px';
    wrapper.style.height = '100%';
    wrapper.style.display = 'flex';
    wrapper.style.flexDirection = 'column';
    
    const content = document.createElement('div');
    content.style.flex = '1';
    content.style.textAlign = 'justify';
    content.style.lineHeight = '1.8';
    content.style.fontSize = '15px';
    content.style.color = '#333';
    
    const heading = document.createElement('h3');
    heading.style.color = 'var(--navy)';
    heading.style.marginBottom = '20px';
    heading.style.fontFamily = 'var(--font-serif)';
    heading.textContent = pageNum + '-sahifa';
    
    const p1 = document.createElement('p');
    p1.style.marginBottom = '15px';
    p1.textContent = `Bu yerda ${pageNum}-sahifaning matni ko'rsatiladi. Haqiqiy kitob uchun PDF fayldan sahifalarni olish kerak.`;
    
    const p2 = document.createElement('p');
    p2.style.marginBottom = '15px';
    p2.textContent = "Flipbook animatsiyasi ishlayapti - sahifalarni chap yoki o'ng tomonga tortib varaqlay olasiz.";
    
    const p3 = document.createElement('p');
    p3.style.marginBottom = '15px';
    p3.textContent = "Shuningdek, sahifa burchaklarini bosib ham varaqlash mumkin.";
    
    content.appendChild(heading);
    content.appendChild(p1);
    content.appendChild(p2);
    content.appendChild(p3);
    
    const pageNumber = document.createElement('div');
    pageNumber.className = 'page-number';
    pageNumber.style.textAlign = 'center';
    pageNumber.style.paddingTop = '20px';
    pageNumber.style.borderTop = '1px solid #ddd';
    pageNumber.textContent = pageNum;
    
    wrapper.appendChild(content);
    wrapper.appendChild(pageNumber);
    pageContent.appendChild(wrapper);
    pageDiv.appendChild(pageContent);
    
    return pageDiv;
}

function createBackCoverPage(bookISBN) {
    const pageDiv = document.createElement('div');
    pageDiv.className = 'page page--cover';
    pageDiv.setAttribute('data-density', 'hard');
    
    const pageContent = document.createElement('div');
    pageContent.className = 'page-content';
    pageContent.style.background = 'linear-gradient(135deg, var(--gold) 0%, var(--navy) 100%)';
    pageContent.style.color = 'white';
    pageContent.style.padding = '60px';
    pageContent.style.position = 'relative';
    
    const title = document.createElement('h2');
    title.style.fontSize = '28px';
    title.style.marginBottom = '30px';
    title.style.textAlign = 'center';
    title.style.fontFamily = 'var(--font-serif)';
    title.textContent = "O'zbek Tilshunosi";
    
    const centerDiv = document.createElement('div');
    centerDiv.style.textAlign = 'center';
    centerDiv.style.marginTop = '100px';
    
    const description = document.createElement('p');
    description.style.fontSize = '16px';
    description.style.opacity = '0.9';
    description.style.lineHeight = '1.8';
    description.innerHTML = "Tilshunoslik sohasidagi fundamental asarlar<br>O'zbek tili va adabiyoti bo'yicha tadqiqotlar";
    
    centerDiv.appendChild(description);
    
    const bottomDiv = document.createElement('div');
    bottomDiv.style.position = 'absolute';
    bottomDiv.style.bottom = '40px';
    bottomDiv.style.left = '0';
    bottomDiv.style.right = '0';
    bottomDiv.style.textAlign = 'center';
    
    const isbn = document.createElement('p');
    isbn.style.fontSize = '14px';
    isbn.style.opacity = '0.8';
    isbn.textContent = 'ISBN: ' + bookISBN;
    
    bottomDiv.appendChild(isbn);
    
    pageContent.appendChild(title);
    pageContent.appendChild(centerDiv);
    pageContent.appendChild(bottomDiv);
    pageDiv.appendChild(pageContent);
    
    return pageDiv;
}

function updateButtons(currentPage, totalPages) {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (prevBtn && nextBtn) {
        prevBtn.disabled = currentPage === 0;
        nextBtn.disabled = currentPage >= totalPages + 1;
    }
}
