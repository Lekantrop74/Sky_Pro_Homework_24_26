from rest_framework import serializers
import re


class VideoLinkValidator:

    def __call__(self, value):
        if value and not re.match(r'^https?://(?:www\.)?youtube\.com/', value):
            raise serializers.ValidationError("Допустимы только ссылки на youtube.com")
