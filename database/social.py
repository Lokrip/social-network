import uuid

from datetime import timedelta

from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.templatetags.static import static
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from database.models import DateModel


class PostTags(DateModel):
    name = models.CharField(_("post tag name"), max_length=120) 
    slug = models.SlugField(
        _('post slug'),
        blank=True,
        help_text=_('Unique tag ID for URL'),
        unique=True
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    
    class Meta:
        ordering = ['name']
        
        verbose_name = _('Post Tag')
        verbose_name_plural = _('Post Tags')
    

class Post(DateModel):
    class Status(models.TextChoices):
        DRAFT = ('draft', _('Draft'))
        PUBLISHED = ('published', _('Published'))
        ARCHIVED = ('archived', _('Archived'))
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('post user')
    )
    post_tag = models.ManyToManyField(
        PostTags, 
        related_name='post',
        blank=True,
        verbose_name=_('post tag'),
        help_text=_('Теги для поста')
    )
    title = models.CharField(_("post title"), max_length=120)
    content = models.TextField(
        _('description'), 
        blank=True, 
        default="Your description"
    )
    status = models.CharField(
        _('status'),
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )
    views = models.PositiveBigIntegerField(_('Post View'), default=0, blank=True)
    
    slug = models.SlugField(
        _('post slug'),
        blank=True,
        help_text=_('Unique tag ID for URL'),
        unique=True
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def get_video(self):
        if self.product_video.video:
            return self.product_video.video.url
        return None
        
    @property
    def get_image(self):
        images = self.product_images.all()

        if images.exists():
            return images[0].image.url
        return static('images/default-image.png')
        
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        
        indexes = [
            models.Index(fields=['title']), 
            models.Index(fields=['slug'])
        ]


class PostImages(DateModel):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        verbose_name=_('post'),
        related_name='product_images',
        blank=True,
        null=True
    )
    image = models.ImageField(
        _('post image'), 
        upload_to="post/image/",
        blank=True,
        null=True,
    )

    
    @property
    def get_image(self):
        try:
            image = self.image.url
        except:
            image = static('images/default-image.png')
        return image

    class Meta:
        verbose_name = 'Post Image'
        verbose_name_plural = 'Post Images'


class PostVideo(models.Model):
    post = models.OneToOneField(
        Post, 
        on_delete=models.CASCADE, 
        related_name='product_video'
    )
    
    video = models.FileField(
        _('post video'),
        upload_to="post/video/",
        blank=True,
        null=True
    )
    
    video_image = models.ImageField(
        _('video image'), 
        upload_to="post/image-video/",
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.post.title} - {self.video.url}"
    
    class Meta:
        verbose_name = 'Post Video'
        verbose_name_plural = 'Post Videos'
    
    @property
    def get_video(self):
        if not self.video:
            return None
        return self.video.url


class Story(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    image = models.ImageField(
        _('post image'), 
        upload_to="stories/images/%Y/%m/%d/",
        blank=True,
        null=True
    )
    video = models.FileField(
        _('stories video'),
        upload_to="stories/videos/%Y/%m/%d/",
        blank=True,
    )
    
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    expires_at = models.DateTimeField()
    seen_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="seen_stories", blank=True)
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
            
    def is_expired(self):
        return timezone.now() > self.expires_at


class StoryView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    story = models.ForeignKey(Story, on_delete=models.CASCADE, verbose_name=_('Story view'))
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} -> {self.story.text}"


class Notification(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_requests',
        verbose_name=_('sender')
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_requests',
        verbose_name=_('recipient')
    )
    content = models.TextField(_('content'))
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', _('Pending')),
            ('accepted', _('Accepted')),
            ('rejected', _('Rejected')),
        ],
        default='pending',
        verbose_name=_('status')
    )
    NOTIFICATION_TYPES = [
        ('comment', _('Comment')),
        ('like', _('Like')),
        ('message', _('Message')),
        ('send_friend', _("Send Friend"))
    ]
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='message',
        verbose_name=_('type')
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}"
    
    def get_type_display(self):
        return dict(self.NOTIFICATION_TYPES).get(self.type) # dict(NOTIFICATION_TYPES) -> {"send_friend": "Send Friend"} -> get to send_friend -> Send Friend
    
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
   
    
class Friendship(DateModel):
    class Status(models.TextChoices):
        REQUESTED = 'requested', _('Запрос отправлен')
        ACCEPTED = 'accepted', _('Принято')
        DECLINED = 'declined', _('Отклонено')
        BLOCKED = 'blocked', _('Заблокировано')
        
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  
        related_name="friendships_initiated",
        verbose_name=_("Отправитель")
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  
        related_name="friendships_received",
        verbose_name=_("Получатель")
    )
    status = models.TextField(
        max_length=10,
        choices=Status.choices,
        default=Status.REQUESTED,
        verbose_name=_("Статус")
    )

    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"

    class Meta:
        unique_together = ('from_user', 'to_user')
        verbose_name = _("Friend")
        verbose_name_plural = _("Friendship")
    
    def accept(self):
        if self.status == self.Status.REQUESTED:
            self.status = self.Status.ACCEPTED
            self.save()
            return True
        return False
    
    def decline(self):
        if self.status == self.Status.REQUESTED:
            self.status = self.Status.DECLINED
            self.save()
            return True
        return False
    
    def blocked(self):
        if self.status in {
            self.Status.REQUESTED, 
            self.Status.ACCEPTED
        }:
            self.status = self.Status.BLOCKED
            self.save()
            return True
        return False
    
    @classmethod
    def create_request(cls, from_user, to_user):
        if not from_user or not to_user:
            raise ValueError("Пользователь не найден")
        
        if (from_user.username == to_user.username 
            or from_user.pk == to_user.pk
            ): raise ValueError("Нельзя отправить запрос самому себе.")
        
        friendship, created = cls.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
            defaults={"status": cls.Status.REQUESTED}
        )
        
        if not created:
            raise ValueError("Запрос уже существует.")
        
        return friendship, created


class FriendshipManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Friendship.Status.ACCEPTED
        )
   
        
class MyFriendshipProxy(Friendship):
    class Meta:
        proxy = True

    objects = FriendshipManager()
    
    
class ChatGroup(models.Model):
    group_name = models.UUIDField(
        _("group name"), 
        max_length=128, 
        unique=True, 
        default=uuid.uuid4,
        editable=False,
    )
    
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="chat_groups", 
        blank=True,
        verbose_name=_("members")
    )
    
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.pk)
    
    def save(self, *args, **kwargs):
        if not self.group_name:
            self.group_name = uuid.uuid4()
        super().save(*args, **kwargs)

    def is_user_member(self, user):
        """Проверка, является ли пользователь членом группы"""
        return user in self.members.all()
  
        
class GroupMessage(DateModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name="group_message", 
        on_delete=models.CASCADE,
        verbose_name=_('user message')
    )
    
    group = models.ForeignKey(
        ChatGroup,
        on_delete=models.CASCADE,
        related_name="group_message",
        verbose_name=_('group')
    )
    
    body = models.CharField(_('body'), max_length=300)
    
    def __str__(self):
        return  f"{self.user.username} : {self.body}"
    
    class Meta:
        ordering = ['-created_at']
        
        verbose_name = 'Group message'
        verbose_name_plural = 'Group messages'