from rest_framework import serializers
from imr_grid_api.models import Post
import cloudinary.uploader



class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Post
        fields = [
            'id', 
            'user', 
            'title', 
            'description', 
            'image', 
            'image_url', 
            'status', 
            'created_at'
        ]
        read_only_fields = ['user', 'image_url', 'created_at']

    
    def create(self, validated_data):
        user = self.context['request'].user
        image_file = validated_data.pop('image', None)

        if image_file:
            try:
                upload_result = cloudinary.uploader.upload(image_file, folder="artistic-grid/posts")
                validated_data['image_url'] = upload_result.get('secure_url')
            except Exception as e:
                raise serializers.ValidationError({"image": "Upload failed. Try again later."})

        post = Post.objects.create(user=user, **validated_data)
        return post