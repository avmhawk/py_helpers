# encoding: utf-8
import functools
import time


def mem(max_size=None, max_time=None):
    def memoize(obj):
        # TODO: можно добавить модуль, который бы читал/писал кэши в файлы "опционально"
        # TODO: возможно, стоит различать ф-ции с хешируемым набором параметров и с не хешируемым
        # и по разному организовать для них хранение пары ключ - кэш
        cache_order = obj.cache_order = []
        cache = obj.cache = {}

        @functools.wraps(obj)
        def memoizer(*args, **kwargs):
            key = str(args) + str(kwargs)
            add_key_to_cache = False
            if key not in cache:
                add_key_to_cache = True
            # если есть какие-то ограничения по размеру или времени хранения кэша:
            elif max_size or max_time:
                if max_size and len(cache_order) > max_size:
                    # если очередь великовата - убиваем элемент, к которому дольше всего не обращались:
                    add_key_to_cache = True
                    cache[cache_order[0]].discard()
                    del cache_order[0]
                if max_time and (time.time() - cache[key]['time']) > max_time:
                    # если "протухло по времени", убиваем:
                    add_key_to_cache = True
                    cache.pop(key, None)
                    cache_order.remove(key)
            if add_key_to_cache:
                cache[key] = {'result': obj(*args, **kwargs), 'time': time.time()}
                # заполнять "очередь" имеет смысл только, если у нас выставлено ограничение:
                if max_size:
                    cache_order.append(key)
            elif max_size:
                # передвигаем вызванную ф-цию в конец списка ("продлеваем" для нее кэш), то есть чем чаще
                # ф-ция используется с такими параметрами, тем меньше у нее шансов выпасть из кэша:
                cache_order.remove(key)
                cache_order.append(key)
            return cache[key]
        return memoizer
    return memoize
