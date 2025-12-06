import io
from flask import Flask, render_template, redirect, request, url_for, send_file
import psycopg2

def ligar_banco():
    banco = psycopg2.connect(
        host='localhost',
        dbname='Retesp4Linhas',
        user='postgres',
        password='senai',
    )
    return banco

app = Flask(__name__)


@app.get('/')
def index():
    banco = ligar_banco()
    cursor = banco.cursor()
    try:
        cursor.execute("""
            SELECT id_atleta, nome_completo, apelido
            FROM lista_atleta
            ORDER BY nome_completo
        """)
        atletas = cursor.fetchall()
        cursor.execute('SELECT COUNT(*) FROM lista_atleta')
        pessoas_ativas = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM lista_espera')
        lista_espera = cursor.fetchone()[0]
        cursor.execute("""
            SELECT COUNT(*)
            FROM lista_atleta
            WHERE id_atleta IN (
                SELECT id_atleta
                FROM falta
                GROUP BY id_atleta
                HAVING COUNT(*) >= 2
            )
        """)
        faltas_atingidas = cursor.fetchone()[0]
        banco.close()
        return render_template('index.html',atletas=atletas, pessoas_ativas=pessoas_ativas, lista_espera=lista_espera, faltas_atingidas=faltas_atingidas)
    except Exception as e:
        print('❌ ERRO AO CARREGAR INDEX:', e)
        cursor.close()
        banco.close()
        return 'Erro ao carregar página', 400


@app.route('/registrar_faltas', methods=['POST'])
def registrar_faltas():
    banco = ligar_banco()
    cursor = banco.cursor()

    try:
        presentes = request.form.getlist('presenca')
        presentes = [int(p) for p in presentes]
        cursor.execute('SELECT id_atleta FROM lista_atleta')
        todos = [row[0] for row in cursor.fetchall()]
        ausentes = [id_a for id_a in todos if id_a not in presentes]
        for id_a in ausentes:
            cursor.execute('INSERT INTO falta (id_atleta) VALUES (%s)', (id_a,))

        banco.commit()
        cursor.close()
        banco.close()

        return redirect(url_for('index'))

    except Exception as erro:
        print('❌ ERRO AO REGISTRAR FALTAS:', erro)
        banco.rollback()
        cursor.close()
        banco.close()
        return 'Erro ao registrar faltas', 400


@app.get('/cadastro')
def cadastro():
    return render_template('formulario.html', destino='salvar_participante')

@app.route('/salvar_participante', methods=['POST'])
def salvar_participante():
    banco = ligar_banco()
    cursor = banco.cursor()
    nome_completo = request.form.get('nome_completo')
    apelido = request.form.get('apelido')
    sexo = request.form.get('sexo')
    data_nascimento = request.form.get('data_nascimento')
    nacionalidade = request.form.get('nacionalidade')
    naturalidade = request.form.get('naturalidade')
    identidade = request.form.get('identidade')
    orgao_exp = request.form.get('orgao_expedidor')
    cpf = request.form.get('cpf')
    pai = request.form.get('pai')
    mae = request.form.get('mae')
    endereco = request.form.get('endereco')
    numero_endereco = request.form.get('numero')
    complemento = request.form.get('complemento')
    bairro = request.form.get('bairro')
    cep = request.form.get('cep')
    municipio = request.form.get('municipio')
    uf = request.form.get('uf')
    fone = request.form.get('fone')
    email = request.form.get('email')
    foto = request.files['foto'].read() if request.files.get('foto') else None
    autorizacao = request.files['autorizacao'].read() if request.files.get('autorizacao') else None
    exame_medico = request.files['exame_medico'].read() if request.files.get('exame_medico') else None
    try:
        cursor.execute("""
            INSERT INTO lista_atleta (
                nome_completo, apelido, sexo, data_nascimento, nacionalidade,
                naturalidade, identidade, orgao_exp, cpf, pai, mae, endereco,
                numero_endereco, complemento, bairro, cep, municipio, uf,
                fone, email, foto, autorizacao, exame_medico
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            nome_completo, apelido, sexo, data_nascimento, nacionalidade,
            naturalidade, identidade, orgao_exp, cpf, pai, mae, endereco,
            numero_endereco, complemento, bairro, cep, municipio, uf,
            fone, email,
            psycopg2.Binary(foto) if foto else None,
            psycopg2.Binary(autorizacao) if autorizacao else None,
            psycopg2.Binary(exame_medico) if exame_medico else None
        ))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect(url_for('index'))

    except Exception as erro:
        print('\n❌ ERRO AO SALVAR:', erro)
        banco.rollback()
        cursor.close()
        banco.close()
        return 'Erro ao salvar participante', 400


@app.get('/editar_participante/<int:id_atleta>')
def editar_participante(id_atleta):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM lista_atleta WHERE id_atleta = %s', (id_atleta,))
    participante = cursor.fetchone()
    cursor.close()
    banco.close()
    return render_template('formulario.html', destino='atualizar_participante', participante=participante)

@app.route('/atualizar_participante', methods=['POST'])
def atualizar_participante():
    banco = ligar_banco()
    cursor = banco.cursor()
    id_atleta = request.form.get('id_universal')
    nome_completo = request.form.get('nome_completo')
    apelido = request.form.get('apelido')
    sexo = request.form.get('sexo')
    data_nascimento = request.form.get('data_nascimento')
    nacionalidade = request.form.get('nacionalidade')
    naturalidade = request.form.get('naturalidade')
    identidade = request.form.get('identidade')
    orgao_exp = request.form.get('orgao_expedidor')
    cpf = request.form.get('cpf')
    pai = request.form.get('pai')
    mae = request.form.get('mae')
    endereco = request.form.get('endereco')
    numero_endereco = request.form.get('numero')
    complemento = request.form.get('complemento')
    bairro = request.form.get('bairro')
    cep = request.form.get('cep')
    municipio = request.form.get('municipio')
    uf = request.form.get('uf')
    fone = request.form.get('fone')
    email = request.form.get('email')
    foto = request.files['foto'].read() if request.files.get('foto') and request.files['foto'].filename != "" else None
    autorizacao = request.files['autorizacao'].read() if request.files.get('autorizacao') and request.files['autorizacao'].filename != "" else None
    exame_medico = request.files['exame_medico'].read() if request.files.get('exame_medico') and request.files['exame_medico'].filename != "" else None

    try:
        update_sql = """
            UPDATE lista_atleta SET
                nome_completo = %s,
                apelido = %s,
                sexo = %s,
                data_nascimento = %s,
                nacionalidade = %s,
                naturalidade = %s,
                identidade = %s,
                orgao_exp = %s,
                cpf = %s,
                pai = %s,
                mae = %s,
                endereco = %s,
                numero_endereco = %s,
                complemento = %s,
                bairro = %s,
                cep = %s,
                municipio = %s,
                uf = %s,
                fone = %s,
                email = %s
        """

        valores = [
            nome_completo, apelido, sexo, data_nascimento, nacionalidade,
            naturalidade, identidade, orgao_exp, cpf, pai, mae, endereco,
            numero_endereco, complemento, bairro, cep, municipio, uf,
            fone, email
        ]
        if foto is not None:
            update_sql += ', foto = %s'
            valores.append(psycopg2.Binary(foto))

        if autorizacao is not None:
            update_sql += ', autorizacao = %s'
            valores.append(psycopg2.Binary(autorizacao))

        if exame_medico is not None:
            update_sql += ', exame_medico = %s'
            valores.append(psycopg2.Binary(exame_medico))

        update_sql += ' WHERE id_atleta = %s'
        valores.append(id_atleta)

        cursor.execute(update_sql, valores)
        banco.commit()
        cursor.close()
        banco.close()
        return redirect(url_for('index'))

    except Exception as erro:
        print('\n❌ ERRO AO ATUALIZAR:', erro)
        banco.rollback()
        cursor.close()
        banco.close()
        return 'Erro ao atualizar participante', 400

@app.route('/excluir/<id_atleta>', methods=['GET', 'DELETE'])
def deletar(id_atleta):
    banco = ligar_banco()
    cursor = banco.cursor()
    try:
        cursor.execute('DELETE FROM lista_atleta WHERE id_atleta=%s;', (id_atleta,))
        banco.commit()
        return redirect(url_for('index'))
    except Exception as erro:
        banco.rollback()
        print('\n❌ ERRO AO EXCLUIR:', erro)
        return 'Erro ao excluir registro', 400

@app.get('/lista_espera')
def lista_espera():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""
                SELECT id_espera, nome_completo, apelido
                FROM lista_espera
                ORDER BY id_espera
            """)
    atletas_espera = cursor.fetchall()
    banco.close()
    cursor.close()
    return render_template('lista_espera.html', atletas_espera=atletas_espera)

@app.get('/cadastro_espera')
def cadastro_espera():
    return render_template('formulario.html', destino='salvar_espera')


@app.route('/salvar_espera', methods=['POST'])
def salvar_espera():
    banco = ligar_banco()
    cursor = banco.cursor()
    nome_completo = request.form.get('nome_completo')
    apelido = request.form.get('apelido')
    sexo = request.form.get('sexo')
    data_nascimento = request.form.get('data_nascimento')
    nacionalidade = request.form.get('nacionalidade')
    naturalidade = request.form.get('naturalidade')
    identidade = request.form.get('identidade')
    orgao_exp = request.form.get('orgao_expedidor')
    cpf = request.form.get('cpf')
    pai = request.form.get('pai')
    mae = request.form.get('mae')
    endereco = request.form.get('endereco')
    numero_endereco = request.form.get('numero')
    complemento = request.form.get('complemento')
    bairro = request.form.get('bairro')
    cep = request.form.get('cep')
    municipio = request.form.get('municipio')
    uf = request.form.get('uf')
    fone = request.form.get('fone')
    email = request.form.get('email')
    foto = request.files['foto'].read() if request.files.get('foto') else None
    autorizacao = request.files['autorizacao'].read() if request.files.get('autorizacao') else None
    exame_medico = request.files['exame_medico'].read() if request.files.get('exame_medico') else None

    try:
        cursor.execute("""
            INSERT INTO lista_espera (
                nome_completo, apelido, sexo, data_nascimento, nacionalidade,
                naturalidade, identidade, orgao_exp, cpf, pai, mae, endereco,
                numero_endereco, complemento, bairro, cep, municipio, uf,
                fone, email, foto, autorizacao, exame_medico
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s)
        """, (
            nome_completo, apelido, sexo, data_nascimento, nacionalidade,
            naturalidade, identidade, orgao_exp, cpf, pai, mae, endereco,
            numero_endereco, complemento, bairro, cep, municipio, uf,
            fone, email,
            psycopg2.Binary(foto) if foto else None,
            psycopg2.Binary(autorizacao) if autorizacao else None,
            psycopg2.Binary(exame_medico) if exame_medico else None
        ))

        banco.commit()
        cursor.close()
        banco.close()
        return redirect(url_for('lista_espera'))

    except Exception as erro:
        print('\n❌ ERRO AO SALVAR NA LISTA DE ESPERA:', erro)
        banco.rollback()
        cursor.close()
        banco.close()
        return 'Erro ao salvar na lista de espera', 400


@app.get('/editar_espera/<id_espera>')
def editar_espera(id_espera):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute('SELECT * FROM lista_espera WHERE id_espera = %s', (id_espera,))
    participante = cursor.fetchone()

    cursor.close()
    banco.close()

    return render_template('formulario.html', participante=participante, destino='atualizar_espera')

@app.route('/atualizar_espera', methods=['POST'])
def atualizar_espera():
    banco = ligar_banco()
    cursor = banco.cursor()

    id_universal = request.form.get('id_universal')
    nome_completo = request.form.get('nome_completo')
    apelido = request.form.get('apelido')
    sexo = request.form.get('sexo')
    data_nascimento = request.form.get('data_nascimento')
    nacionalidade = request.form.get('nacionalidade')
    naturalidade = request.form.get('naturalidade')
    identidade = request.form.get('identidade')
    orgao_exp = request.form.get('orgao_expedidor')
    cpf = request.form.get('cpf')
    pai = request.form.get('pai')
    mae = request.form.get('mae')
    endereco = request.form.get('endereco')
    numero_endereco = request.form.get('numero')
    complemento = request.form.get('complemento')
    bairro = request.form.get('bairro')
    cep = request.form.get('cep')
    municipio = request.form.get('municipio')
    uf = request.form.get('uf')
    fone = request.form.get('fone')
    email = request.form.get('email')
    foto = request.files['foto'].read() if request.files.get('foto') and request.files['foto'].filename != "" else None
    autorizacao = request.files['autorizacao'].read() if request.files.get('autorizacao') and request.files['autorizacao'].filename != "" else None
    exame_medico = request.files['exame_medico'].read() if request.files.get('exame_medico') and request.files['exame_medico'].filename != "" else None
    try:
        cursor.execute("""
            SELECT foto, autorizacao, exame_medico
            FROM lista_espera
            WHERE id_espera = %s
        """, (id_universal,))
        atual = cursor.fetchone()
        foto_atual, autorizacao_atual, exame_atual = atual
        update_sql = """
            UPDATE lista_espera SET
                nome_completo = %s,
                apelido = %s,
                sexo = %s,
                data_nascimento = %s,
                nacionalidade = %s,
                naturalidade = %s,
                identidade = %s,
                orgao_exp = %s,
                cpf = %s,
                pai = %s,
                mae = %s,
                endereco = %s,
                numero_endereco = %s,
                complemento = %s,
                bairro = %s,
                cep = %s,
                municipio = %s,
                uf = %s,
                fone = %s,
                email = %s,
                foto = %s,
                autorizacao = %s,
                exame_medico = %s
            WHERE id_espera = %s
        """

        valores = [
            nome_completo, apelido, sexo, data_nascimento, nacionalidade,
            naturalidade, identidade, orgao_exp, cpf, pai, mae, endereco,
            numero_endereco, complemento, bairro, cep, municipio, uf,
            fone, email,
            psycopg2.Binary(foto) if foto else foto_atual,
            psycopg2.Binary(autorizacao) if autorizacao else autorizacao_atual,
            psycopg2.Binary(exame_medico) if exame_medico else exame_atual,
            id_universal
        ]

        cursor.execute(update_sql, valores)
        banco.commit()
        cursor.close()
        banco.close()
        return redirect(url_for('lista_espera'))

    except Exception as erro:
        print('\n❌ ERRO AO ATUALIZAR LISTA DE ESPERA:', erro)
        banco.rollback()
        cursor.close()
        banco.close()
        return 'Erro ao atualizar', 400


@app.route('/excluir_espera/<id_espera>', methods=['GET', 'POST'])
def deletar_espera(id_espera):
    banco = ligar_banco()
    cursor = banco.cursor()

    try:
        cursor.execute('DELETE FROM lista_espera WHERE id_espera=%s;', (id_espera,))
        banco.commit()
        return redirect(url_for('lista_espera'))
    except Exception as erro:
        banco.rollback()
        print('\n❌ ERRO AO EXCLUIR:', erro)
        return 'Erro ao excluir registro', 400


@app.route('/adicionar_lista/<int:id_espera>', methods=['GET'])
def adicionar_lista(id_espera):
    banco = ligar_banco()
    cursor = banco.cursor()

    try:
        cursor.execute('SELECT * FROM lista_espera WHERE id_espera = %s', (id_espera,))
        participante = cursor.fetchone()

        if not participante:
            cursor.close()
            banco.close()
            return 'Participante não encontrado', 404
        cursor.execute("""
            INSERT INTO lista_atleta (
                nome_completo, apelido, sexo, data_nascimento, nacionalidade,
                naturalidade, identidade, orgao_exp, cpf, pai, mae, endereco,
                numero_endereco, complemento, bairro, cep, municipio, uf,
                fone, email, foto, autorizacao, exame_medico
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            participante[1], participante[2], participante[3], participante[4], participante[5],
            participante[6], participante[7], participante[8], participante[9], participante[10],
            participante[11], participante[12], participante[13], participante[14], participante[15],
            participante[16], participante[17], participante[18], participante[19], participante[20],
            participante[21], participante[22], participante[23]
        ))
        cursor.execute('DELETE FROM lista_espera WHERE id_espera = %s', (id_espera,))

        banco.commit()
        cursor.close()
        banco.close()

        return redirect(url_for('lista_espera'))

    except Exception as erro:
        print('❌ ERRO AO ADICIONAR NA LISTA PRINCIPAL:', erro)
        banco.rollback()
        cursor.close()
        banco.close()
        return 'Erro ao adicionar participante', 400

@app.get('/faltas')
def faltas():
    banco = ligar_banco()
    cursor = banco.cursor()

    try:
        cursor.execute("""
            SELECT id_atleta, nome_completo, apelido
            FROM lista_atleta
            WHERE id_atleta IN (
                SELECT id_atleta
                FROM falta
                GROUP BY id_atleta
                HAVING COUNT(*) >= 2
            )
            ORDER BY nome_completo
        """)
        atletas_falta = cursor.fetchall()

        cursor.close()
        banco.close()

        return render_template('faltas.html', atletas_falta=atletas_falta)

    except Exception as e:
        print('❌ ERRO AO CARREGAR FALTAS:', e)
        banco.rollback()
        cursor.close()
        banco.close()
        return 'Erro ao carregar página de faltas', 400

@app.route('/desconsiderar/<int:id_atleta>', methods=['GET'])
def desconsiderar(id_atleta):
    banco = ligar_banco()
    cursor = banco.cursor()
    try:
        cursor.execute('DELETE FROM falta WHERE id_atleta = %s', (id_atleta,))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect(url_for('faltas'))
    except Exception as e:
        print('❌ ERRO AO DESCONSIDERAR FALTAS:', e)
        banco.rollback()
        cursor.close()
        banco.close()
        return 'Erro ao desconsiderar faltas', 400

@app.route('/remover_atleta_falta/<int:id_atleta>', methods=['GET'])
def remover_atleta_falta(id_atleta):
    banco = ligar_banco()
    cursor = banco.cursor()
    try:
        cursor.execute('DELETE FROM falta WHERE id_atleta = %s', (id_atleta,))
        cursor.execute('DELETE FROM lista_atleta WHERE id_atleta = %s', (id_atleta,))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect(url_for('faltas'))
    except Exception as e:
        print('❌ ERRO AO REMOVER ATLETA:', e)
        banco.rollback()
        cursor.close()
        banco.close()
        return 'Erro ao remover atleta', 400

@app.get('/ver_participante/<tabela>/<int:id>')
def ver_participante(tabela, id):
    banco = ligar_banco()
    cursor = banco.cursor()
    if tabela not in ('lista_atleta', 'lista_espera'):
        return 'Tabela inválida', 400
    cursor.execute(f"""
        SELECT *
        FROM {tabela}
        WHERE {'id_atleta' if tabela == 'lista_atleta' else 'id_espera'} = %s
    """, (id,))
    participante = cursor.fetchone()
    cursor.close()
    banco.close()
    if not participante:
        return 'Participante não encontrado', 404
    return render_template('ver_participante.html', participante=participante, tabela=tabela)


def recuperar_foto(id_pessoa, tabela, campo):
    banco = ligar_banco()
    cursor = banco.cursor()
    chave = 'id_atleta' if tabela == 'lista_atleta' else 'id_espera'
    query = f'SELECT {campo} FROM {tabela} WHERE {chave} = %s'
    cursor.execute(query, (id_pessoa,))
    resultado = cursor.fetchone()
    if resultado and resultado[0]:
        return resultado[0]
    return None



@app.route('/imagem/<tabela>/<campo>/<int:id_pessoa>')
def imagem(tabela, campo, id_pessoa):
    foto_blob = recuperar_foto(id_pessoa, tabela, campo)
    if foto_blob is None:
        return send_file('static/sem_foto.jpg', mimetype='image/jpeg')
    return send_file(
        io.BytesIO(bytes(foto_blob)),
        mimetype='image/jpeg',
        download_name=f'{campo}_{id_pessoa}.jpg'
    )




if __name__ == '__main__':
    app.run()
