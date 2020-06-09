class StorageService():
	import cloudinary

	storage_service = cloudinary.uploader

	@staticmethod
	def check_if_storage_service_is_set():
		if not StorageService.storage_service:
			raise ValueError('StorageService instance is not set')

	@staticmethod
	def set_instance(storage_service):
		StorageService.storage_service = storage_service

	@staticmethod
	def get_instance():
		return StorageService.storage_service

	@staticmethod
	def upload(*args, **kwargs):
		StorageService.check_if_storage_service_is_set()
		return StorageService.storage_service.upload(*args, **kwargs)

	@staticmethod
	def destroy(*args, **kwargs):
		StorageService.check_if_storage_service_is_set()
		return StorageService.storage_service.destroy(*args,**kwargs)
