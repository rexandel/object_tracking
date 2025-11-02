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
| cars_moving | Справляется до выхода за границы | Теряет через пару секунд | Теряет через пару секунд | **CSRT** |
| dribbling_ball | Теряет мяч, переключается на похожий объект | Полностью теряет объект | Теряет мяч, переключается на шорты | **CSRT** |
| people_walking | Справляется до выхода за границы | Справляется до выхода за границы | Справляется до выхода за границы | **Ничья** |
| street_walking | Справляется с небольшим смещением | Справляется со средним смещением | Справляется с большим смещением | **CSRT** |
| surfer | Справляется до конца видео | Справляется до конца видео | Справляется до конца видео | **Ничья** |

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

- В `видео 2` вместо полной потери объекта собственная реализация переключается на похожий объект
- В `видео 4` позволяет сделать выделяемую область меньшего размера, но при этом отслеживание объекта происходит корректно

### Использование собственной реализации KCF

<div style="white-space: nowrap;">
  <img src="https://github.com/user-attachments/assets/84d92089-ad62-4a35-b52b-4c778887d186" width="300" style="display: inline-block;">
  <img src="https://github.com/user-attachments/assets/aba96230-6f2f-4aae-9cca-0540c34c4e05" width="300" style="display: inline-block;">
  <img src="https://github.com/user-attachments/assets/9dc2ee8e-a614-49d3-9935-96f92b4d5620" width="300" style="display: inline-block;">
</div>

## Установка зависимостей

Перед запуском проекта необходимо установить зависимости:

```bash
pip install -r requirements.txt
```

Требования к версии Python: `Python 3.8+`
