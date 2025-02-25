// GitPy JavaScript

// ファイルツリーの展開・折りたたみ機能
document.addEventListener('DOMContentLoaded', function() {
    // ファイルツリーの折りたたみ機能
    const folders = document.querySelectorAll('.file-folder');
    folders.forEach(folder => {
        folder.addEventListener('click', function() {
            const subFolder = this.nextElementSibling;
            if (subFolder && subFolder.tagName === 'UL') {
                subFolder.classList.toggle('d-none');
                // アイコンの切り替え
                const icon = this.querySelector('i');
                if (icon) {
                    if (icon.classList.contains('fa-folder-open')) {
                        icon.classList.replace('fa-folder-open', 'fa-folder');
                    } else {
                        icon.classList.replace('fa-folder', 'fa-folder-open');
                    }
                }
            }
        });
    });
    
    // コードエディタの高さ自動調整
    const codeTextareas = document.querySelectorAll('.code-editor');
    codeTextareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        // 初期高さの設定
        textarea.dispatchEvent(new Event('input'));
    });
});
