from celery import shared_task
from .models import Video

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)

    # Store the video file in Amazon S3
    s3_key = f'videos/{video_file.name}'
    s3_client.upload_file(file_path, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

    # Extract subtitles using ccextractor
    subtitle_file = os.path.join(settings.MEDIA_ROOT, 'subtitles.srt')
    ccextractor_cmd = f'ccextractor "{file_path}" -o "{subtitle_file}"'
    subprocess.run(ccextractor_cmd, shell=True)

    # Apply subtitles and save the processed video to Amazon S3
    processed_video_key = f'processed_videos/{video_file.name}'
    processed_video_url = os.path.join(settings.MEDIA_URL, processed_video_key)
    processed_video_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': processed_video_key},
        ExpiresIn=3600  # URL expiration time in seconds (optional)
    )
    
    # Store the processed video in Amazon S3
    s3_client.upload_file(file_path, settings.AWS_STORAGE_BUCKET_NAME, processed_video_key)


    # Store extracted search keywords in DynamoDB
    with open(subtitle_file, 'r') as f:
        keywords = f.read()
        start_time = subtitle.start
        end_time = subtitle.end
    # dynamodb_client.put_item(
    #     TableName='search_keywords',
    #     Item={
    #         'video_name': {'S': video_file.name},
    #         'keywords': {'S': keywords}
    #     }
    # )

    # Create a Video object in the database
    video = Video.objects.create(video_file=video_file,processed_file = processed_video_key, subtitles=keywords, start_time=start_time, end_time=end_time)

    # Save the video object, which will trigger the creation/update of the corresponding record in the database
    video.save()

    # Update the Video model with the processed video details    
    # video.subtitles = video.subtitles
    # video.processed_file = processed_video_key
    # video.start_time = video.start_time
    # video.end_time = video.end_time    
    # video.save()
    return render(request, 'processing.html', {'processed_video_url': processed_video_url})
