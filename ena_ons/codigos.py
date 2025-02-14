"""Módulo para códigos que precisam ser hardcoded."""

from pydantic import BaseModel


class Codigos(BaseModel):
    """Códigos necessários para gerar vazões artificiais."""

    traicao: int = 104
    guarapiranga: int = 117
    billings: int = 118
    billings_artificial: int = 319
    billings_pedras: int = 119
    edgard_souza_com_tributarios: int = 161
    edgard_souza_sem_tributarios: int = 164
    pedras: int = 116
    pedreira: int = 109
    henry_borden: int = 318
    barra_bonita: int = 237
    barra_bonita_artificial: int = 37
    bariri: int = 238
    bariri_artificial: int = 38
    ibitinga: int = 239
    ibitinga_artificial: int = 39
    promissao: int = 240
    promissao_artificial: int = 40
    nova_avanhandava: int = 242
    nova_avanhandava_artificial: int = 42
    tres_irmaos: int = 243
    tres_irmaos_artificial: int = 43
    ilha_solteira: int = 34
    ilha_solteira_equiv: int = 44
    jupia: int = 245
    jupia_artificial: int = 45
    porto_primavera: int = 246
    porto_primavera_artificial: int = 46
    itaipu: int = 266
    itaipu_artificial: int = 66
    santa_cecilia: int = 125
    bombeamento_santa_cecilia: int = 298
    anta: int = 129
    santana: int = 203
    santana_vertimento: int = 304
    santana_artificial: int = 315
    anta_artificial: int = 127
    tocos: int = 201
    vertimento_tocos: int = 317
    vigario: int = 316
    simplicio_artificial: int = 126
    ilha_pombos: int = 130
    ilha_pombos_artificial: int = 299
    nilo_pecanha_artificial: int = 131
    lajes_artificial: int = 132
    lajes: int = 202
    fontes_artificial: int = 303
    pereira_passos_artificial: int = 306
    camargos: int = 1
    itutinga: int = 2
    moxoto: int = 173
    paulo_afonso: int = 175
    complexo: int = 176
    jordao: int = 73
    jordao_artificial: int = 70
    segredo: int = 76
    segredo_artificial: int = 75
    itiquira1: int = 259
    itiquira2: int = 252
    pimental: int = 288
    belo_monte_artificial: int = 292
    pimental_artificial: int = 302


codigos = Codigos()
