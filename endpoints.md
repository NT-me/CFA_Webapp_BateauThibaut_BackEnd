# Endpoints

## Informations produits

| Enpoints                                                     | Méthode                       | Json type                                                    |
| ------------------------------------------------------------ | ----------------------------- | ------------------------------------------------------------ |
| products/info/{id}                                           | GET                           | {<br/>  "id": 1,<br/>  "name": "Filet Bar de ligne",<br/>  "category": 0,<br/>  "price": 7,<br/>  "unit": "2 filets",<br/>  "availability": true,<br/>  "sale": true,<br/>  "discount": 5.6000000000000005,<br/>  "comments": "environ 300g",<br/>  "owner": "tig",<br/>  "quantityInStock": 40<br/>} |
| products/info/all                                            | GET                           | [<br />{<br/>  "id": 1,<br/>  "name": "Filet Bar de ligne",<br/>  "category": 0,<br/>  "price": 7,<br/>  "unit": "2 filets",<br/>  "availability": true,<br/>  "sale": true,<br/>  "discount": 5.6000000000000005,<br/>  "comments": "environ 300g",<br/>  "owner": "tig",<br/>  "quantityInStock": 40<br/>},<br />{...}<br />] |
| products/info/all?category={cat_id}&availability={bool}&sale={bool} | GET<br />Arguments optionnels | [<br />{<br/>  "id": 1,<br/>  "name": "Filet Bar de ligne",<br/>  "category": 0,<br/>  "price": 7,<br/>  "unit": "2 filets",<br/>  "availability": true,<br/>  "sale": true,<br/>  "discount": 5.6000000000000005,<br/>  "comments": "environ 300g",<br/>  "owner": "tig",<br/>  "quantityInStock": 40<br/>},<br />{...}<br />]                                                       |
|                                                              |                               | `json`                                                       |
|                                                              |                               | `json`                                                       |
|                                                              |                               | `json`                                                       |
|                                                              |                               | `json`                                                       |

## Gestion produits
| Enpoints  | Méthode                                                      | Json type                                                    |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| products/ | POST<br />Avec sans doute un header spécifique car auth nécessaire<br />```json ``` :<br />[<br /> {<br />	id : *int* <br />	stock : *Optionnal int*<br />	discPer : *Optionnal Int*<br /> } <br />] | {<br/>  "status": "success",<br/>  "New state": [<br/>    {<br/>      "id": 12,<br/>      "discountPercentage": 90,<br/>      "discount": 9,<br/>      "quantityInStock": 102,<br/>      "availability": true<br/>    }<br/>  ]<br/>} |
|           |                                                              | `json`                                                       |
|           |                                                              | `json`                                                       |
|           |                                                              | `json`                                                       |
|           |                                                              | `json`                                                       |
|           |                                                              | `json`                                                       |

## Gestion Identification
| Enpoints | Méthode | Json type |
| -------- | ------- | --------- |
|          |         | `json`    |
|          |         | `json`    |
|          |         | `json`    |
|          |         | `json`    |
|          |         | `json`    |
|          |         | `json`    |
|          |         | `json`    |
|          |         | `json`    |
|          |         | `json`    |

