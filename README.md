## О проекте

Данный проект предназначен для сравнительного анализа различных алгоритмов корреляционного трекинга объектов на видео. Исследуются три популярных трекера:
* CSRT (Channel and Spatial Reliability Tracker)
* KCF (Kernelized Correlation Filters)
* MOSSE (Minimum Output Sum of Squared Error)

Сначала были [исследованы](https://github.com/rexandel/object_tracking/tree/main/cv2_trackers) встроенные в OpenCV реализации трекеров, затем KCF-трекер был [реализован вручную](https://github.com/rexandel/object_tracking/blob/main/homemade_kcf/kcf_tracker.py). 

### Список видео

* `cars_moving.mp4` ([YouTube](https://www.youtube.com/watch?v=Y1jTEyb3wiI))
* `dribbling_ball.mp4` ([YouTube](https://www.youtube.com/watch?v=retWHRQjQGg))
* `people_walking.mp4` ([YouTube](https://www.youtube.com/watch?v=ORrrKXGx2SE))
* `street_walking.mp4` ([YouTube](https://www.youtube.com/watch?v=Mol0lrRBy3g))
* `surfer.mp4` ([YouTube](https://www.youtube.com/watch?v=yJfHvFZhBxg))

Подробнее о видео: [video_description.md](https://github.com/rexandel/object_tracking/blob/main/videos/video_description.md)

### Результаты тестирования

**Презентация**: [presentation.pdf](https://github.com/rexandel/object_tracking/blob/main/presentation.pdf)

| Видео | CSRT | KCF | MOSSE | Победитель |
|-------|------|-----|-------|------------|
| `cars_moving` | Справляется до выхода за границы | Теряет через пару секунд | Теряет через пару секунд | **CSRT** |
| `dribbling_ball` | Теряет мяч, переключается на похожий объект | Полностью теряет объект | Теряет мяч, переключается на шорты | **CSRT** |
| `people_walking` | Справляется до выхода за границы | Справляется до выхода за границы | Справляется до выхода за границы | **Ничья** |
| `street_walking` | Справляется с небольшим смещением | Справляется со средним смещением | Справляется с большим смещением | **CSRT** |
| `surfer` | Справляется до конца видео | Справляется до конца видео | Справляется до конца видео | **Ничья** |

### Сравнительная характеристика алгоритмов

#### CSRT
- **Преимущества**: лучшая точность отслеживания
- **Недостатки**: низкая скорость работы

#### KCF
- **Преимущества**: устойчивость к помехам и фонам
- **Недостатки**: чувствителен к быстрым изменениям

#### MOSSE
- **Преимущества**: высокая скорость и простота
- **Недостатки**: чувствителен к окклюзиям, ограниченность адаптивности

### Собственная реализация KCF

Собственная реализация метода не только не уступает по точности аналогу из библиотеки OpenCV, но даже превосходит в некоторых ситуациях:

- В видео `dribbling_ball` вместо полной потери объекта собственная реализация переключается на похожий объект
- В видео `street_walking` позволяет сделать выделяемую область меньшего размера, но при этом отслеживание объекта происходит корректно

## Установка зависимостей

Перед запуском проекта необходимо установить зависимости:

```bash
pip install -r requirements.txt
```

Требования к версии Python: `Python 3.8+`
