from ...application.use_case.image import ImageUseCase
from ...domain.model.image import ImageDomain
from ...infrastructure.mongo.repositories.image_mongo import ImageMongo


class ImageController:
    def __init__(
        self,
        image_path,
        ref_write_uid,
        ref_repository,
        ref_broker,
    ) -> None:
        self._p = image_path
        _w = ref_write_uid
        _r = ImageMongo(ref_repository)
        _b = ref_broker
        self._uc = ImageUseCase(_w, _r, _b)

    def create(
        self,
        image_file,
        image_id,
    ):
        image_id = ImageDomain.set_identifier(image_id)
        obj = ImageDomain.new(
            image_file,
            image_id,
            self._p,
        )

        return self._uc.create(obj)
