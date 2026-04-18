from django.db import models


class Researcher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Pathogen(models.Model):

    TRANSMISSION_CHOICES = [
        ('blood', 'Кровь'),
        ('water', 'Вода'),
        ('air', 'Воздух'),
        ('contact', 'Контакт'),
        ('food', 'Пища'),
        ('vector', 'Насекомые (вектор)'),
    ]
    TRANSMISSION_LABELS = {
    "water vector": "Водный путь",
    "airborne": "Воздушно-капельный",
    "contact": "Контактный",
    "blood": "Через кровь",
}
    def get_transmission_display_list(self):
        labels = {
        "water vector": "Водный путь",
        "airborne": "Воздушно-капельный",
        "contact": "Контактный",
        "blood": "Через кровь",
    }
        return [labels.get(x, x) for x in self.transmission]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='pathogens/', blank=True, null=True)

    author = models.ForeignKey(
        Researcher,
        on_delete=models.CASCADE,
        related_name='pathogens'
    )

    creator = models.ForeignKey(
        Researcher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_pathogens'
    )

    family = models.CharField(max_length=100, blank=True)
    origin = models.CharField(max_length=100, blank=True)
    discovered = models.CharField(max_length=100, blank=True)
    application = models.CharField(max_length=200, blank=True)

    transmission = models.JSONField(default=list, blank=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title