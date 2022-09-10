"""Celery start """

from email_sender.tasks import app

if __name__ == "__main__":
    argv = [
        'worker',
        '-B',
        '--loglevel=DEBUG',
        '--without-heartbeat',
        '--without-mingle',
        '--without-gossip',
        '--queues=send_emails'
    ]
    app.worker_main(argv)
