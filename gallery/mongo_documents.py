import json
from datetime import datetime
from bson.objectid import ObjectId

from django.conf import settings

rendition_sizes = [25, 150, 480, 1080, 1920]


# def create_photo(photo: dict):



# class Photo:
#     id: ObjectId
#     title: str
#     uuid: str
#     category_id: int
#     filenames: {int: str}
#     img_ratio: float
#     user_id: int
#     created_at: datetime
#     updated_at: datetime
#     deleted_at: datetime = None
#
#     def to_json(self):
#         return json.dumps({
#             'title': self.title,
#             'uuid': self.uuid,
#             'filenames': self.filenames,
#             'img_ratio': self.img_ratio,
#             'user_id': self.user_id,
#             'updated_at': self.updated_at,
#             'deleted_at': self.deleted_at,
#         })
#
#     def get_document(self):
#         db = settings.MONGO
#         return db.photos[f'user_{self.user_id}'][f'category_{self.category_id}']
#
#     def create(self):
#         photos = self.get_document()
#         self.id = photos.insert_one(self.to_json()).inserted_id
#         return self.id
