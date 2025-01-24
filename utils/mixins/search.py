from django.contrib.postgres.search import (
    SearchRank,
    SearchQuery,
    SearchVector,
)

from .utils import LoggerUtils

class Search(LoggerUtils):
    __slots__ = ('model', 'query')
    
    def __init__(self, model, query):
        self.model = model
        self.query = query
        
    def search(self):
        """
        Выполняет полнотекстовый поиск по заданной модели.

        Returns:
            QuerySet: Результаты поиска.

        Raises:
            ValueError: Если модель не определена или возникли проблемы при поиске.
            Exception: При других непредвиденных ошибках.
        """
        
        if not self.model:
            raise ValueError(
                self.logger(topic='database')[0]
            )
        
        try:
            vector = SearchVector(
                'title', 
                'content'
            )
            query = SearchQuery(self.query)
            
            # rank в контексте полнотекстового поиска в Django (и в общем в системах поиска) означает 
            # оценку (или рейтинг) релевантности результата поиска. Он показывает, насколько хорошо 
            # документ (или запись в базе данных) соответствует заданному запросу
            results = self.model.objects.annotate(
                rank=SearchRank(vector, query)
            ).filter(
                rank__gt=0).order_by(
                    '-rank').select_related('user').prefetch_related(
                        'product_images',
                        'product_video'
                    )
            
            return results

        except Exception as e:
            # Ловим все непредвиденные ошибки и пробрасываем их дальше
            raise Exception(
                f"An unexpected error occurred: {
                    str(e)}"
            )
            
        except ValueError as VE:
            if VE in self.logger(topic='search'):
                raise VE