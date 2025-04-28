from fastapi import APIRouter, Depends, HTTPException
from fastapi import Path
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db.models.article import Article
from backend.db.models.user import User
from backend.schemas.article import ArticleCreate, ArticleOut
from backend.dependencies.auth import get_current_user
from typing import List

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.post("/", response_model=ArticleOut)
def create_article(
        article: ArticleCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    """
    Crea un artículo en la base de datos.

    **Parámetros**
    - El contenido del artículo a crear:

    - `article`: El titulo del articulo
    - `hash`: Una key del articulo
    - `date`: Fecha de publicacion
    - `copyright`: Autor o contribuciones

    **Respuesta**
    - El artículo recién creado con su `ID`.
    """
    db_article = Article(**article.dict(), user_id=user.id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.get("/", response_model=List[ArticleOut])
def get_articles(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    """
    Obtiene todos los artículos del usuario actual, excluyendo los eliminados.

    **Respuesta**
    - Lista de artículos del usuario que no han sido marcados como eliminados, `deleted` is False.
    """
    return db.query(Article).filter(Article.user_id == user.id, Article.deleted == False).all()


@router.put("/{article_id}", response_model=ArticleOut)
def delete_article(
        article_id: int = Path(..., description="ID of the article to edit"),
        status: bool = True,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    """
    Marca un artículo como eliminado sin borrarlo físicamente.

    **Parámetros**
    - `article_id`: El ID del artículo.
    - `status`: El status (false => eliminado, true => activo).

    **Respuesta**
    - El artículo con su campo `deleted` actualizado.
    """
    db_article = db.query(Article).filter(Article.id == article_id, Article.user_id == user.id).first()

    if db_article is None:
        raise HTTPException(status_code=404, detail="Artículo no encontrado.")

    db_article.deleted = status
    db.commit()
    db.refresh(db_article)

    return db_article
