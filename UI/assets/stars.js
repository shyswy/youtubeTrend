// 별똥별(은하수 느낌) 애니메이션
const STAR_COUNT = 25;
const MIN_DURATION = 2; // 초
const MAX_DURATION = 6; // 초
const TWINKLE_STAR_COUNT = 150;

function randomBetween(a, b) {
    return a + Math.random() * (b - a);
}

function createTwinkleStars() {
    for (let i = 0; i < TWINKLE_STAR_COUNT; i++) {
        const star = document.createElement('div');
        let className = 'twinkle-star';
        const r = Math.random();
        if (r < 0.10) className += ' big';
        else if (r < 0.20) className += ' blue';
        else if (r < 0.30) className += ' purple';
        else if (r < 0.40) className += ' yellow';
        star.className = className;
        const size = (className.includes('big')) ? 4 : randomBetween(1, 2.5);
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        // 전체 화면에 고르게 분포
        const left = randomBetween(0, 100);
        const top = randomBetween(0, 100);
        star.style.left = left + 'vw';
        star.style.top = top + 'vh';
        star.style.opacity = randomBetween(0.3, 1).toFixed(2);
        star.style.animationDuration = randomBetween(1.5, 4) + 's';
        star.style.animationDelay = randomBetween(0, 3) + 's';
        document.body.appendChild(star);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    createTwinkleStars();
}); 