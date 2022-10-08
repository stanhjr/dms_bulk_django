config = {
    'imports': ('celery_tasks.tasks',),
    'database_engine_options': {'echo': False},
    'worker_concurrency': 2,
    'task_acks_late': True,
    'task_annotations': {
        'celery_tasks.tasks.send_verify_link_to_email': {
            'queue': 'celery_tasks'
        },
        'celery_tasks.tasks.send_welcome_to_dmsbulk_message_after_success_verifing' : {
            'queue': 'celery_tasks'
        },
        'celery_tasks.tasks.send_reset_password_link_to_email': {
            'queue': 'celery_tasks'
        },
        'celery_tasks.delete_order_from_actives': {
            'queue': 'celery_tasks'
        },
        'celery_tasks.update_analytics': {
            'queue': 'celery_tasks'
        },
    },
    'accept_content': ['json', 'application/x-python-serialize'],
    'task_serializer': 'json',
    'result_serializer': 'json',
    'event_serializer': 'json',
    'result_expires': 7200,
    'task_compression': 'gzip',
    'result_compression': 'gzip',
    'task_default_queue': 'celery_tasks',
    'redis_max_connections': 2,
    'broker_transport_options': {
        'max_connections': 2
    },
    'broker_pool_limit': 2
}
