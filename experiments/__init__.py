__all__ = ['network', 'wallet']


def init(bot):
    for i in __all__:
        bot.load_extension(f'experiments.{i}')
